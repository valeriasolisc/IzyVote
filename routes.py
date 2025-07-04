from flask import render_template, request, redirect, url_for, flash, session, jsonify
from app import app, db
from models import Election, VerificationCode, VoterHistory
from blockchain import voting_blockchain
from email_service import email_service
import hashlib
import os
from datetime import datetime, timedelta, timezone
import json

# Zona horaria de Perú (UTC-5)
PERU_TZ = timezone(timedelta(hours=-5))

@app.route('/')
def index():
    """Página principal con elecciones activas"""
    active_elections = Election.query.filter_by(is_active=True).all()
    return render_template('index.html', elections=active_elections)

@app.route('/verify_email/<int:election_id>', methods=['GET', 'POST'])
def verify_email(election_id):
    """Página de verificación de correo"""
    election = Election.query.get_or_404(election_id)
    
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        
        # Valida dominios universitarios
        allowed_domains = ['@uni.pe', '@uni.edu.pe', '@unmsm.edu.pe']
        if not any(email.endswith(domain) for domain in allowed_domains):
            flash('Solo se permiten correos de los dominios @uni.pe o @uni.edu.pe', 'error')
            return render_template('verify_email.html', election=election)
        
        # Verifica que el usuario no haya votado ya
        email_hash = hashlib.sha256(email.encode()).hexdigest()
        existing_vote = VoterHistory.query.filter_by(
            email_hash=email_hash, 
            election_id=election_id
        ).first()
        
        if existing_vote:
            flash('Ya has votado en esta elección.', 'error')
            return redirect(url_for('index'))
        
        # Genera y envía código de verificación
        verification_code = email_service.generate_verification_code()
        
        # Verifica si ya existe un código para este correo y elección
        verification = VerificationCode(
            email=email,
            code=verification_code,
            election_id=election_id
        )
        db.session.add(verification)
        db.session.commit()
        
        # Envía correo de verificación
        if email_service.send_verification_email(email, verification_code, election.title):
            session['verification_id'] = verification.id
            flash('Código de verificación enviado a tu correo.', 'success')
            return redirect(url_for('vote', election_id=election_id))
        else:
            flash('Error enviando el código. Intenta de nuevo.', 'error')
    
    return render_template('verify_email.html', election=election)

@app.route('/vote/<int:election_id>', methods=['GET', 'POST'])
def vote(election_id):
    """Página de votación"""
    election = Election.query.get_or_404(election_id)
    
    if not election.is_active:
        flash('Esta elección no está activa.', 'error')
        return redirect(url_for('index'))
    
    verification_id = session.get('verification_id')
    if not verification_id:
        return redirect(url_for('verify_email', election_id=election_id))
    
    verification = VerificationCode.query.get(verification_id)
    if not verification or verification.used or verification.election_id != election_id:
        flash('Código de verificación inválido.', 'error')
        return redirect(url_for('verify_email', election_id=election_id))
    
    # Verifica que el código no haya expirado (30 minutos)
    now_peru = datetime.now(PERU_TZ).replace(tzinfo=None)
    if now_peru - verification.created_at > timedelta(minutes=30):
        flash('Código de verificación expirado.', 'error')
        return redirect(url_for('verify_email', election_id=election_id))
    
    if request.method == 'POST':
        code = request.form.get('code', '').strip()
        selected_option = request.form.get('option', '').strip()
        
        if code != verification.code:
            flash('Código de verificación incorrecto.', 'error')
            return render_template('vote.html', election=election, options=election.get_options())
        
        if not selected_option or selected_option not in election.get_options():
            flash('Opción de voto inválida.', 'error')
            return render_template('vote.html', election=election, options=election.get_options())
        
        # Marca el código como usado
        verification.used = True
        
        # Crea historial de voto
        email_hash = hashlib.sha256(verification.email.encode()).hexdigest()
        voter_history = VoterHistory(
            email_hash=email_hash,
            election_id=election_id
        )
        
        # Añade voto a la blockchain
        voting_blockchain.add_vote(election_id, selected_option)
        voting_blockchain.mine_pending_votes()
        
        db.session.add(voter_history)
        db.session.commit()
        
        # Envía correo de confirmación
        email_service.send_vote_confirmation(verification.email, election.title)
        
        # Cierra sesión de verificación
        session.pop('verification_id', None)
        
        flash('¡Voto registrado exitosamente!', 'success')
        return redirect(url_for('results', election_id=election_id))
    
    return render_template('vote.html', election=election, options=election.get_options())

@app.route('/results/<int:election_id>')
def results(election_id):
    """Pagina de resultados de votación"""
    election = Election.query.get_or_404(election_id)
    vote_count = voting_blockchain.get_vote_count(election_id)
    
    # Asegura que todas las opciones estén representadas
    options = election.get_options()
    for option in options:
        if option not in vote_count:
            vote_count[option] = 0
    
    return render_template('results.html', election=election, vote_count=vote_count)

@app.route('/blockchain')
def blockchain_view():
    """Mira la cadena de bloques"""
    blockchain_data = voting_blockchain.to_dict()
    return render_template('blockchain_view.html', blockchain=blockchain_data)

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    """Pagina de login para el admin"""
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '').strip()
        
        admin_email = os.environ.get('ADMIN_EMAIL', 'valeria.solis.c@uni.pe')
        admin_password = os.environ.get('ADMIN_PASSWORD', 'PruebaDeSoftware')
        
        if email == admin_email and password == admin_password:
            session['admin_logged_in'] = True
            flash('Bienvenido al panel administrativo.', 'success')
            return redirect(url_for('admin_panel'))
        else:
            flash('Credenciales incorrectas.', 'error')
    
    return render_template('admin_login.html')

@app.route('/admin/panel', methods=['GET', 'POST'])
def admin_panel():
    """Panel de administración"""
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    
    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'create_election':
            title = request.form.get('title', '').strip()
            description = request.form.get('description', '').strip()
            options_text = request.form.get('options', '').strip()
            
            if not title or not options_text:
                flash('Título y opciones son requeridos.', 'error')
            else:
                options = [opt.strip() for opt in options_text.split('\n') if opt.strip()]
                if len(options) < 2:
                    flash('Se requieren al menos 2 opciones.', 'error')
                else:
                    election = Election(
                        title=title,
                        description=description
                    )
                    election.set_options(options)
                    db.session.add(election)
                    db.session.commit()
                    flash('Elección creada exitosamente.', 'success')
        
        elif action == 'toggle_election':
            election_id = request.form.get('election_id')
            election = Election.query.get(election_id)
            if election:
                election.is_active = not election.is_active
                db.session.commit()
                status = 'activada' if election.is_active else 'desactivada'
                flash(f'Elección {status} exitosamente.', 'success')
        
        elif action == 'delete_election':
            election_id = request.form.get('election_id')
            election = Election.query.get(election_id)
            if election:
                # Eliminar códigos de verificación asociados
                VerificationCode.query.filter_by(election_id=election_id).delete()
                # Eliminar historial de votantes
                VoterHistory.query.filter_by(election_id=election_id).delete()
                # Eliminar la elección
                db.session.delete(election)
                db.session.commit()
                
                # Eliminar votos de la blockchain
                voting_blockchain.remove_votes_for_election(int(election_id))
                
                flash(f'Elección "{election.title}" eliminada exitosamente.', 'success')
    
    elections = Election.query.order_by(Election.created_at.desc()).all()
    return render_template('admin_panel.html', elections=elections, voting_blockchain=voting_blockchain)

@app.route('/admin/logout')
def admin_logout():
    """Admin logout"""
    session.pop('admin_logged_in', None)
    flash('Sesión cerrada exitosamente.', 'success')
    return redirect(url_for('index'))

@app.route('/api/results/<int:election_id>')
def api_results(election_id):
    """API devuelve los resultados de votación en formato JSON."""
    vote_count = voting_blockchain.get_vote_count(election_id)
    election = Election.query.get_or_404(election_id)
    
    # Asegura que todas las opciones estén representadas
    options = election.get_options()
    for option in options:
        if option not in vote_count:
            vote_count[option] = 0
    
    return jsonify(vote_count)

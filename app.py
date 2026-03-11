"""
Citizen Grievance Management Portal
Flask Backend Application
"""

from flask import Flask, render_template, redirect, url_for, request, flash, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'cgmp-secret-key-2024'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cgmp.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SESSION_TYPE'] = 'filesystem'
app.config['UPLOAD_FOLDER'] = os.path.join('static', 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # 10MB max file size
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif', 'mp4', 'avi', 'mov'}

# Create upload folder if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Initialize session
from flask.sessions import SecureCookieSessionInterface
app.session_interface = SecureCookieSessionInterface()

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# ==================== Translations ====================
translations = {
    'en': {
        # Navigation
        'home': 'Home', 'features': 'Features', 'how_it_works': 'How It Works', 'categories': 'Categories',
        'login': 'Login', 'register': 'Register', 'logout': 'Logout', 'dashboard': 'Dashboard',
        'submit_complaint': 'Submit Complaint', 'track_complaint': 'Track Complaint',
        'feedback': 'Feedback', 'manage_officials': 'Manage Officials', 'reports': 'Reports',
        # Home page
        'hero_title': 'Citizen Grievance Management Portal',
        'hero_desc': 'Report civic issues effortlessly and track their resolution. Connect with government authorities and make your voice heard for a better community.',
        'register_complaint': 'Register Complaint', 'key_features': 'Key Features', 'how_it_works_title': 'How It Works',
        'complaint_categories': 'Complaint Categories', 'complaints_resolved': 'Complaints Resolved',
        'active_citizens': 'Active Citizens', 'govt_departments': 'Government Departments',
        'location_based': 'Location-Based Reporting', 'location_desc': 'Report issues with precise GPS location or map-based tagging for accurate identification of problem areas.',
        'real_time': 'Real-Time Tracking', 'real_time_desc': 'Track your complaint status in real-time from submission to resolution with unique complaint IDs.',
        'instant_notif': 'Instant Notifications', 'notif_desc': 'Receive updates at every stage of your complaint resolution process via the portal.',
        'feedback_system': 'Feedback System', 'feedback_desc': 'Rate the resolution quality and provide feedback to help improve government services.',
        'data_analytics': 'Data Analytics', 'analytics_desc': 'Authorities can analyze complaint patterns to make data-driven decisions for better service delivery.',
        'secure_transparent': 'Secure & Transparent', 'secure_desc': 'Complete transparency in the grievance resolution process with secure user authentication.',
        'step1': 'Register', 'step1_desc': 'Create an account on the portal with your basic details',
        'step2': 'Submit Issue', 'step2_desc': 'Report the civic issue with description and location',
        'step3': 'Track Progress', 'step3_desc': 'Monitor your complaint status in real-time',
        'step4': 'Get Resolution', 'step4_desc': 'Receive resolution and provide feedback',
        'roads': 'Roads', 'water': 'Water', 'electricity': 'Electricity', 'waste': 'Waste', 'safety': 'Safety', 'others': 'Others',
        'quick_links': 'Quick Links', 'contact_support': 'Contact Support', 'back_to_home': 'Back to Home',
        # Dashboard
        'welcome': 'Welcome', 'total_complaints': 'Total Complaints', 'in_progress': 'In Progress', 'resolved': 'Resolved',
        'pending': 'Pending', 'your_complaints': 'Your Complaints', 'new_complaint': 'New Complaint',
        'no_complaints': 'No complaints yet', 'submit_first': 'Submit your first complaint to get started',
        'assigned_complaints': 'Assigned Complaints', 'view': 'View', 'update': 'Update', 'assign': 'Assign',
        'recent_complaints': 'Recent Complaints', 'admin_dashboard': 'Admin Dashboard', 'citizen_portal': 'Citizen Portal',
        'official_portal': 'Official Portal', 'add_new_official': 'Add New Official', 'existing_officials': 'Existing Officials',
        'reports_analytics': 'Reports & Analytics', 'category_distribution': 'Category Distribution',
        'status_distribution': 'Status Distribution', 'monthly_trends': 'Monthly Trends',
        # Forms
        'email': 'Email Address', 'password': 'Password', 'full_name': 'Full Name', 'phone': 'Phone Number',
'i_am_a': 'I am a', 'citizen': 'Citizen', 'govt_official': 'Government Assigned Workers', 'department': 'Department',
        'title': 'Title', 'description': 'Description', 'location': 'Location', 'category': 'Category',
        'status': 'Status', 'remarks': 'Remarks', 'rating': 'Rating', 'submit': 'Submit', 'cancel': 'Cancel',
        'submit_complaint_title': 'Submit New Complaint', 'brief_title': 'Brief title of the issue',
        'describe_issue': 'Describe the issue in detail', 'enter_address': 'Enter address or click on map',
        'pin_location': 'Pin Location on Map (Optional)',
        # Complaint
        'complaint_id': 'Complaint ID', 'submitted': 'Submitted', 'under_review': 'Under Review',
        'assigned': 'Assigned', 'in_progress_status': 'In Progress', 'complaint_timeline': 'Complaint Timeline',
        'current_status': 'Current Status', 'give_feedback': 'Give Feedback',
        'rate_experience': 'Rate Your Experience', 'complaint_resolved': 'Your complaint has been resolved',
        'share_experience': 'Share your experience...', 'submit_feedback': 'Submit Feedback',
        'update_complaint': 'Update Complaint', 'update_status': 'Update Status',
        'add_official': 'Add Official', 'name': 'Name',
        'no_account': "Don't have an account? ", 'register_here': 'Register here',
    },
    'hi': {
        # Navigation
        'home': 'होम', 'features': 'विशेषताएं', 'how_it_works': 'कैसे काम करता है', 'categories': 'श्रेणियां',
        'login': 'लॉगिन', 'register': 'रजिस्टर', 'logout': 'लॉगआउट', 'dashboard': 'डैशबोर्ड',
        'submit_complaint': 'शिकायत दर्ज करें', 'track_complaint': 'शिकायत ट्रैक करें',
        'feedback': 'प्रतिक्रिया', 'manage_officials': 'अधिकारी प्रबंधन', 'reports': 'रिपोर्ट',
        # Home page
        'hero_title': 'नागरिक शिकायत प्रबंधन पोर्टल',
        'hero_desc': 'नागरिक मुद्दों को आसानी से रिपोर्ट करें और उनके समाधान को ट्रैक करें। बेहतर समुदाय के लिए अपनी आवाज सुनाने के लिए सरकारी अधिकारियों से जुड़ें।',
        'register_complaint': 'शिकायत दर्ज करें', 'key_features': 'मुख्य विशेषताएं', 'how_it_works_title': 'कैसे काम करता है',
        'complaint_categories': 'शिकायत श्रेणियां', 'complaints_resolved': 'शिकायतें हल की गईं',
        'active_citizens': 'सक्रिय नागरिक', 'govt_departments': 'सरकारी विभाग',
        'location_based': 'स्थान-आधारित रिपोर्टिंग', 'location_desc': 'समस्या क्षेत्रों की सटीक पहचान के लिए सटीक GPS स्थान या मानचित्र-आधारित टैगिंग के साथ समस्याओं की रिपोर्ट करें।',
        'real_time': 'रीयल-टाइम ट्रैकिंग', 'real_time_desc': 'अद्वितीय शिकायत ID के साथ सबमिशन से समाधान तक अपनी शिकायत की स्थिति को रीयल-टाइम में ट्रैक करें।',
        'instant_notif': 'तत्काल सूचनाएं', 'notif_desc': 'पोर्टल के माध्यम से शिकायत समाधान प्रक्रिया के प्रत्येक चरण पर अपडेट प्राप्त करें।',
        'feedback_system': 'प्रतिक्रिया प्रणाली', 'feedback_desc': 'सरकारी सेवाओं को बेहतर बनाने में मदद के लिए समाधान गुणवत्ता को रेट करें और प्रतिक्रिया दें।',
        'data_analytics': 'डेटा विश्लेषण', 'analytics_desc': 'अधिकारी बेहतर सेवा वितरण के लिए डेटा-संचालित निर्णय लेने के लिए शिकायत पैटर्न का विश्लेषण कर सकते हैं।',
        'secure_transparent': 'सुरक्षित और पारदर्शी', 'secure_desc': 'सुरक्षित उपयोगकर्ता प्रमाणीकरण के साथ शिकायत समाधान प्रक्रिया में पूर्ण पारदर्शिता।',
        'step1': 'रजिस्टर', 'step1_desc': 'अपने मूल विवरण के साथ पोर्टल पर एक खाता बनाएं',
        'step2': 'समस्या दर्ज करें', 'step2_desc': 'विवरण और स्थान के साथ नागरिक मुद्दे की रिपोर्ट करें',
        'step3': 'प्रगति ट्रैक करें', 'step3_desc': 'अपनी शिकायत की स्थिति को रीयल-टाइम में देखें',
        'step4': 'समाधान प्राप्त करें', 'step4_desc': 'समाधान प्राप्त करें और प्रतिक्रिया दें',
        'roads': 'सड़कें', 'water': 'पानी', 'electricity': 'बिजली', 'waste': 'कचरा', 'safety': 'सुरक्षा', 'others': 'अन्य',
        'quick_links': 'त्वरित लिंक', 'contact_support': 'सहायता से संपर्क करें', 'back_to_home': 'होम पर वापस जाएं',
        # Dashboard
        'welcome': 'स्वागत है', 'total_complaints': 'कुल शिकायतें', 'in_progress': 'प्रगति में', 'resolved': 'हल हो गई',
        'pending': 'लंबित', 'your_complaints': 'आपकी शिकायतें', 'new_complaint': 'नई शिकायत',
        'no_complaints': 'अभी तक कोई शिकायत नहीं', 'submit_first': 'शुरू करने के लिए अपनी पहली शिकायत दर्ज करें',
        'assigned_complaints': 'सौंपी गई शिकायतें', 'view': 'देखें', 'update': 'अपडेट', 'assign': 'सौंपें',
        'recent_complaints': 'हाल की शिकायतें', 'admin_dashboard': 'एडमिन डैशबोर्ड', 'citizen_portal': 'नागरिक पोर्टल',
        'official_portal': 'अधिकारी पोर्टल', 'add_new_official': 'नया अधिकारी जोड़ें', 'existing_officials': 'मौजूदा अधिकारी',
        'reports_analytics': 'रिपोर्ट और विश्लेषण', 'category_distribution': 'श्रेणी वितरण',
        'status_distribution': 'स्थिति वितरण', 'monthly_trends': 'मासिक रुझान',
        # Forms
        'email': 'ईमेल पता', 'password': 'पासवर्ड', 'full_name': 'पूरा नाम', 'phone': 'फोन नंबर',
        'i_am_a': 'मैं हूं', 'citizen': 'नागरिक', 'govt_official': 'सरकारी अधिकारी', 'department': 'विभाग',
        'title': 'शीर्षक', 'description': 'विवरण', 'location': 'स्थान', 'category': 'श्रेणी',
        'status': 'स्थिति', 'remarks': 'टिप्पणियां', 'rating': 'रेटिंग', 'submit': 'सबमिट', 'cancel': 'रद्द करें',
        'submit_complaint_title': 'नई शिकायत दर्ज करें', 'brief_title': 'मुद्दे का संक्षिप्त शीर्षक',
        'describe_issue': 'मुद्दे का विस्तार से वर्णन करें', 'enter_address': 'पता दर्ज करें या मानचित्र पर क्लिक करें',
        'pin_location': 'मानचित्र पर स्थान पिन करें (वैकल्पिक)',
        # Complaint
        'complaint_id': 'शिकायत आईडी', 'submitted': 'सबमिट किया गया', 'under_review': 'समीक्षा में',
        'assigned': 'सौंपा गया', 'in_progress_status': 'प्रगति में', 'complaint_timeline': 'शिकायत समयरेखा',
        'current_status': 'वर्तमान स्थिति', 'give_feedback': 'प्रतिक्रिया दें',
        'rate_experience': 'अपना अनुभव रेट करें', 'complaint_resolved': 'आपकी शिकायत हल हो गई है',
        'share_experience': 'अपना अनुभव साझा करें...', 'submit_feedback': 'प्रतिक्रिया सबमिट करें',
        'update_complaint': 'शिकायत अपडेट करें', 'update_status': 'स्थिति अपडेट करें',
        'add_official': 'अधिकारी जोड़ें', 'name': 'नाम',
    },
    'es': {
        # Navigation
        'home': 'Inicio', 'features': 'Características', 'how_it_works': 'Cómo funciona', 'categories': 'Categorías',
        'login': 'Iniciar sesión', 'register': 'Registrarse', 'logout': 'Cerrar sesión', 'dashboard': 'Panel',
        'submit_complaint': 'Presentar queja', 'track_complaint': 'Rastrear queja',
        'feedback': 'Comentarios', 'manage_officials': 'Gestionar funcionarios', 'reports': 'Informes',
        # Home page
        'hero_title': 'Portal de Gestión de Reclamaciones Ciudadanas',
        'hero_desc': 'Informe problemas cívicos sin esfuerzo y siga su resolución. Conéctese con las autoridades gubernamentales para mejorar su comunidad.',
        'register_complaint': 'Registrar queja', 'key_features': 'Características principales', 'how_it_works_title': 'Cómo funciona',
        'complaint_categories': 'Categorías de quejas', 'complaints_resolved': 'Quejas resueltas',
        'active_citizens': 'Ciudadanos activos', 'govt_departments': 'Departamentos gubernamentales',
        'location_based': 'Informes basados en ubicación', 'location_desc': 'Informe problemas con ubicación GPS precisa o etiquetado en mapa para una identificación exacta.',
        'real_time': 'Seguimiento en tiempo real', 'real_time_desc': 'Siga el estado de su queja en tiempo real desde el envío hasta la resolución.',
        'instant_notif': 'Notificaciones instantáneas', 'notif_desc': 'Reciba actualizaciones en cada etapa del proceso de resolución de quejas.',
        'feedback_system': 'Sistema de comentarios', 'feedback_desc': 'Califique la calidad de la resolución y proporcione comentarios.',
        'data_analytics': 'Análisis de datos', 'analytics_desc': 'Las autoridades pueden analizar patrones de quejas para decisiones basadas en datos.',
        'secure_transparent': 'Seguro y transparente', 'secure_desc': 'Transparencia total en el proceso de resolución con autenticación segura.',
        'step1': 'Registrarse', 'step1_desc': 'Cree una cuenta en el portal con sus datos básicos',
        'step2': 'Presentar problema', 'step2_desc': 'Reporte el problema cívico con descripción y ubicación',
        'step3': 'Seguir progreso', 'step3_desc': 'Monitoree el estado de su queja en tiempo real',
        'step4': 'Obtener resolución', 'step4_desc': 'Reciba la resolución y proporcione comentarios',
        'roads': 'Caminos', 'water': 'Agua', 'electricity': 'Electricidad', 'waste': 'Residuos', 'safety': 'Seguridad', 'others': 'Otros',
        'quick_links': 'Enlaces rápidos', 'contact_support': 'Contactar soporte', 'back_to_home': 'Volver al inicio',
        # Dashboard
        'welcome': 'Bienvenido', 'total_complaints': 'Total de quejas', 'in_progress': 'En progreso', 'resolved': 'Resueltas',
        'pending': 'Pendientes', 'your_complaints': 'Sus quejas', 'new_complaint': 'Nueva queja',
        'no_complaints': 'Sin quejas aún', 'submit_first': 'Presente su primera queja para comenzar',
        'assigned_complaints': 'Quejas asignadas', 'view': 'Ver', 'update': 'Actualizar', 'assign': 'Asignar',
        'recent_complaints': 'Quejas recientes', 'admin_dashboard': 'Panel de admin', 'citizen_portal': 'Portal ciudadano',
        'official_portal': 'Portal de funcionarios', 'add_new_official': 'Agregar nuevo funcionario', 'existing_officials': 'Funcionarios existentes',
        'reports_analytics': 'Informes y análisis', 'category_distribution': 'Distribución por categoría',
        'status_distribution': 'Distribución por estado', 'monthly_trends': 'Tendencias mensuales',
        # Forms
        'email': 'Correo electrónico', 'password': 'Contraseña', 'full_name': 'Nombre completo', 'phone': 'Número de teléfono',
        'i_am_a': 'Soy un', 'citizen': 'Ciudadano', 'govt_official': 'Funcionario gubernamental', 'department': 'Departamento',
        'title': 'Título', 'description': 'Descripción', 'location': 'Ubicación', 'category': 'Categoría',
        'status': 'Estado', 'remarks': 'Observaciones', 'rating': 'Calificación', 'submit': 'Enviar', 'cancel': 'Cancelar',
        'submit_complaint_title': 'Presentar nueva queja', 'brief_title': 'Título breve del problema',
        'describe_issue': 'Describa el problema en detalle', 'enter_address': 'Ingrese dirección o haga clic en el mapa',
        'pin_location': 'Fijar ubicación en el mapa (Opcional)',
        # Complaint
        'complaint_id': 'ID de queja', 'submitted': 'Enviada', 'under_review': 'En revisión',
        'assigned': 'Asignada', 'in_progress_status': 'En progreso', 'complaint_timeline': 'Línea de tiempo',
        'current_status': 'Estado actual', 'give_feedback': 'Dar comentarios',
        'rate_experience': 'Califique su experiencia', 'complaint_resolved': 'Su queja ha sido resuelta',
        'share_experience': 'Comparta su experiencia...', 'submit_feedback': 'Enviar comentarios',
        'update_complaint': 'Actualizar queja', 'update_status': 'Actualizar estado',
        'add_official': 'Agregar funcionario', 'name': 'Nombre',
    },
    'fr': {
        # Navigation
        'home': 'Accueil', 'features': 'Fonctionnalités', 'how_it_works': 'Comment ça marche', 'categories': 'Catégories',
        'login': 'Connexion', 'register': "S'inscrire", 'logout': 'Déconnexion', 'dashboard': 'Tableau de bord',
        'submit_complaint': 'Déposer une plainte', 'track_complaint': 'Suivre la plainte',
        'feedback': 'Commentaires', 'manage_officials': 'Gérer les officials', 'reports': 'Rapports',
        # Home page
        'hero_title': 'Portail de gestion des réclamations citoyennes',
        'hero_desc': 'Signalez sans effort les problèmes civiques et suivez leur résolution. Connectez-vous avec les autorités gouvernementales pour une meilleure communauté.',
        'register_complaint': 'Enregistrer une plainte', 'key_features': 'Fonctionnalités clés', 'how_it_works_title': 'Comment ça marche',
        'complaint_categories': 'Catégories de plaintes', 'complaints_resolved': 'Plaintes résolues',
        'active_citizens': 'Citizens actifs', 'govt_departments': 'Départements gouvernementaux',
        'location_based': 'Signalement basé sur la localisation', 'location_desc': 'Signalez les problèmes avec une localisation GPS précise ou un marquage sur carte.',
        'real_time': 'Suivi en temps réel', 'real_time_desc': 'Suivez le statut de votre plainte en temps réel du dépôt à la résolution.',
        'instant_notif': 'Notifications instantanées', 'notif_desc': 'Recevez des mises à jour à chaque étape du processus de résolution.',
        'feedback_system': 'Système de commentaires', 'feedback_desc': 'Évaluez la qualité de la résolution et fournissez des commentaires.',
        'data_analytics': 'Analyse de données', 'analytics_desc': 'Les autorités peuvent analyser les modèles de plaintes pour des décisions basées sur les données.',
        'secure_transparent': 'Sécurisé et transparent', 'secure_desc': 'Transparence totale dans le processus de résolution avec authentification sécurisée.',
        'step1': "S'inscrire", 'step1_desc': 'Créez un compte sur le portail avec vos coordonnées',
        'step2': 'Soumettre un problème', 'step2_desc': 'Signalez le problème civic avec description et localisation',
        'step3': 'Suivre les progrès', 'step3_desc': 'Surveillez le statut de votre plainte en temps réel',
        'step4': 'Obtenir la résolution', 'step4_desc': 'Recevez la résolution et fournissez des commentaires',
        'roads': 'Routes', 'water': 'Eau', 'electricity': 'Électricité', 'waste': 'Déchets', 'safety': 'Sécurité', 'others': 'Autres',
        'quick_links': 'Liens rapides', 'contact_support': 'Contacter le support', 'back_to_home': "Retour à l'accueil",
        # Dashboard
        'welcome': 'Bienvenue', 'total_complaints': 'Total des plaintes', 'in_progress': 'En cours', 'resolved': 'Résolues',
        'pending': 'En attente', 'your_complaints': 'Vos plaintes', 'new_complaint': 'Nouvelle plainte',
        'no_complaints': 'Pas encore de plaintes', 'submit_first': 'Déposez votre première plainte pour commencer',
        'assigned_complaints': 'Plaints assignées', 'view': 'Voir', 'update': 'Mettre à jour', 'assign': 'Assigner',
        'recent_complaints': 'Plaints récentes', 'admin_dashboard': 'Tableau admin', 'citizen_portal': 'Portail citoyen',
        'official_portal': 'Portail des officials', 'add_new_official': 'Ajouter un nouvel officiel', 'existing_officials': 'Officials existants',
        'reports_analytics': 'Rapports et analyses', 'category_distribution': 'Distribution par catégorie',
        'status_distribution': 'Distribution par statut', 'monthly_trends': 'Tendances mensuelles',
        # Forms
        'email': 'Adresse e-mail', 'password': 'Mot de passe', 'full_name': 'Nom complet', 'phone': 'Numéro de téléphone',
        'i_am_a': 'Je suis un', 'citizen': 'Citoyen', 'govt_official': 'Officiel gouvernemental', 'department': 'Département',
        'title': 'Titre', 'description': 'Description', 'location': 'Localisation', 'category': 'Catégorie',
        'status': 'Statut', 'remarks': 'Remarques', 'rating': 'Évaluation', 'submit': 'Soumettre', 'cancel': 'Annuler',
        'submit_complaint_title': 'Soumettre une nouvelle plainte', 'brief_title': 'Titre bref du problème',
        'describe_issue': 'Décrivez le problème en détail', 'enter_address': 'Entrez ladresse ou cliquez sur la carte',
        'pin_location': 'Épingler la localisation sur la carte (Optionnel)',
        # Complaint
        'complaint_id': 'ID de plainte', 'submitted': 'Soumise', 'under_review': 'En cours dexamen',
        'assigned': 'Assignée', 'in_progress_status': 'En cours', 'complaint_timeline': 'Chronologie',
        'current_status': 'Statut actuel', 'give_feedback': 'Donner des commentaires',
        'rate_experience': 'Évaluez votre expérience', 'complaint_resolved': 'Votre plainte a été résolue',
        'share_experience': 'Partagez votre expérience...', 'submit_feedback': 'Soumettre les commentaires',
        'update_complaint': 'Mettre à jour la plainte', 'update_status': 'Mettre à jour le statut',
        'add_official': 'Ajouter un officiel', 'name': 'Nom',
    },
    'te': {
        # Navigation - Telugu (తెలుగు)
        'home': 'హోం', 'features': 'ఫీచర్స్', 'how_it_works': 'ఎలా పనిచేస్తుంది', 'categories': 'కేటగరీలు',
        'login': 'లాగिन్', 'register': 'రిజిస్టర్', 'logout': 'లాగ్‌అ웃్', 'dashboard': ' డాష్‌బోర్డ్',
        'submit_complaint': 'ఫిర్యాదు దాఖలు', 'track_complaint': 'ఫిర్యాదు ట్రాక్',
        'feedback': 'ఫీడ్‌బ్యాక్', 'manage_officials': 'అధికారులు నిర్వహణ', 'reports': 'రిపోర్ట్',
        # Home page
        'hero_title': 'నాగరక్ ఫిర్యాదు నిర్వహణ పోర్టల్',
        'hero_desc': 'పౌర సమస్యలను Easily కి Reported చేసుకోండి మరియు వాటి Resolution ట్రాక్. ప్రభుత్వాధికారులతో Connect చేసుకుని మెరుగైన Community కోసం మీ Voice শLYన్.',
        'register_complaint': 'ఫిర్యాదు నమోదు', 'key_features': 'Key Features', 'how_it_works_title': 'ఎలా పనిచేస్తుంది',
        'complaint_categories': 'ఫిర్యాదు Categories', 'complaints_resolved': 'Complaints Resolved',
        'active_citizens': 'Active Citizens', 'govt_departments': 'Government Departments',
        'location_based': 'Location Based Reporting', 'location_desc': 'Problems Precise GPS Location Or Map Based Tagging.',
        'real_time': 'Real Time Tracking', 'real_time_desc': 'Unique Complaint IDs.',
        'instant_notif': 'Instant Notifications', 'notif_desc': 'Portal.',
        'feedback_system': 'Feedback System', 'feedback_desc': 'Government Services.',
        'data_analytics': 'Data Analytics', 'analytics_desc': 'Data-Driven Decisions.',
        'secure_transparent': 'Secure & Transparent', 'secure_desc': 'Secure User Authentication.',
        'step1': 'Register', 'step1_desc': 'Account With Basic Details',
        'step2': 'Submit Issue', 'step2_desc': 'Civic Issue With Description And Location',
        'step3': 'Track Progress', 'step3_desc': 'Complaint Status In Real-Time',
        'step4': 'Get Resolution', 'step4_desc': 'Resolution And Provide Feedback',
        'roads': 'Roads', 'water': 'Water', 'electricity': 'Electricity', 'waste': 'Waste', 'safety': 'Safety', 'others': 'Others',
        'quick_links': 'Quick Links', 'contact_support': 'Contact Support', 'back_to_home': 'Back To Home',
        # Dashboard
        'welcome': 'Welcome', 'total_complaints': 'Total Complaints', 'in_progress': 'In Progress', 'resolved': 'Resolved',
        'pending': 'Pending', 'your_complaints': 'Your Complaints', 'new_complaint': 'New Complaint',
        'no_complaints': 'No Complaints Yet', 'submit_first': 'Submit First Complaint To Get Started',
        'assigned_complaints': 'Assigned Complaints', 'view': 'View', 'update': 'Update', 'assign': 'Assign',
        'recent_complaints': 'Recent Complaints', 'admin_dashboard': 'Admin Dashboard', 'citizen_portal': 'Citizen Portal',
        'official_portal': 'Official Portal', 'add_new_official': 'Add New Official', 'existing_officials': 'Existing Officials',
        'reports_analytics': 'Reports & Analytics', 'category_distribution': 'Category Distribution',
        'status_distribution': 'Status Distribution', 'monthly_trends': 'Monthly Trends',
        # Forms
        'email': 'Email Address', 'password': 'Password', 'full_name': 'Full Name', 'phone': 'Phone Number',
        'i_am_a': 'I Am A', 'citizen': 'Citizen', 'govt_official': 'Govt Official', 'department': 'Department',
        'title': 'Title', 'description': 'Description', 'location': 'Location', 'category': 'Category',
        'status': 'Status', 'remarks': 'Remarks', 'rating': 'Rating', 'submit': 'Submit', 'cancel': 'Cancel',
        'submit_complaint_title': 'Submit New Complaint', 'brief_title': 'Brief Title Of Issue',
        'describe_issue': 'Describe Issue In Detail', 'enter_address': 'Enter Address Or Click On Map',
        'pin_location': 'Pin Location On Map (Optional)',
        # Complaint
        'complaint_id': 'Complaint ID', 'submitted': 'Submitted', 'under_review': 'Under Review',
        'assigned': 'Assigned', 'in_progress_status': 'In Progress', 'complaint_timeline': 'Complaint Timeline',
        'current_status': 'Current Status', 'give_feedback': 'Give Feedback',
        'rate_experience': 'Rate Your Experience', 'complaint_resolved': 'Complaint Resolved',
        'share_experience': 'Share Your Experience...', 'submit_feedback': 'Submit Feedback',
        'update_complaint': 'Update Complaint', 'update_status': 'Update Status',
        'add_official': 'Add Official', 'name': 'Name',
    }
}

def get_translations():
    """Get translations based on current language"""
    lang = session.get('language', 'en')
    return translations.get(lang, translations['en'])

def translate(key):
    """Translate a key to the current language"""
    lang = session.get('language', 'en')
    trans = translations.get(lang, translations['en'])
    return trans.get(key, key)

@app.context_processor
def inject_translations():
    """Make translations available to all templates"""
    return dict(t=translate, current_language=session.get('language', 'en'))

# Language route
@app.route('/set_language/<lang>')
def set_language(lang):
    """Set the language and redirect back to previous page"""
    if lang in ['en', 'hi', 'es', 'fr', 'te']:
        session['language'] = lang
    # Get the referring page or default to index
    return redirect(request.referrer or url_for('index'))

# ==================== Database Models ====================

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # citizen, official, admin
    department = db.Column(db.String(50), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Complaint(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    complaint_id = db.Column(db.String(20), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    division = db.Column(db.String(100), nullable=True)  # Problem Division
    subdivision = db.Column(db.String(200), nullable=True)  # Problem Subdivision
    other_division = db.Column(db.String(200), nullable=True)  # Custom division if "Other"
    other_subdivision = db.Column(db.String(200), nullable=True)  # Custom subdivision if "Other"
    location = db.Column(db.String(300), nullable=False)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    image_path = db.Column(db.String(300), nullable=True)
    admin_image_path = db.Column(db.String(300), nullable=True)  # Admin uploaded evidence
    official_image_path = db.Column(db.String(300), nullable=True)  # Official uploaded evidence
    age = db.Column(db.Integer, nullable=True)
    gender = db.Column(db.String(20), nullable=True)
    status = db.Column(db.String(30), default='Submitted')  # Submitted, Under Review, Assigned, In Progress, Resolved
    assigned_to = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    remarks = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    user = db.relationship('User', foreign_keys=[user_id], backref='complaints')
    assigned_official = db.relationship('User', foreign_keys=[assigned_to])

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    complaint_id = db.Column(db.Integer, db.ForeignKey('complaint.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    feedback_text = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    complaint = db.relationship('Complaint', backref='feedback')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ==================== Routes ====================

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/home')
def home():
    if current_user.is_authenticated:
        if current_user.role == 'admin':
            return redirect(url_for('admin_dashboard'))
        elif current_user.role == 'official':
            return redirect(url_for('official_dashboard'))
        else:
            return redirect(url_for('citizen_dashboard'))
    return redirect(url_for('login'))

# Authentication Routes
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        password = request.form.get('password')
        role = request.form.get('role', 'citizen')
        department = request.form.get('department')
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered', 'error')
            return redirect(url_for('register'))
        
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(name=name, email=email, phone=phone, 
                       password=hashed_password, role=role, department=department)
        db.session.add(new_user)
        db.session.commit()
        
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()
        
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('home'))
        else:
            flash('Invalid email or password', 'error')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

# Citizen Routes
@app.route('/citizen/dashboard')
@login_required
def citizen_dashboard():
    if current_user.role != 'citizen':
        return redirect(url_for('home'))
    
    complaints = Complaint.query.filter_by(user_id=current_user.id).order_by(Complaint.created_at.desc()).all()
    return render_template('citizen_dashboard.html', complaints=complaints)

@app.route('/citizen/submit', methods=['GET', 'POST'])
@login_required
def submit_complaint():
    if current_user.role != 'citizen':
        return redirect(url_for('home'))
    
    if request.method == 'POST':
        # Get Problem Division and Subdivision (now required)
        division = request.form.get('division')
        subdivision = request.form.get('subdivision')
        other_division = request.form.get('other_division')
        other_subdivision = request.form.get('other_subdivision')
        
        # Title and Description are now optional - use subdivision as default
        title = request.form.get('title') or subdivision or "Complaint"
        description = request.form.get('description') or other_subdivision or f"{division} - {subdivision}"
        
        # Get other form fields
        category = request.form.get('category') or division
        location = request.form.get('location')
        latitude = request.form.get('latitude')
        longitude = request.form.get('longitude')
        age = request.form.get('age')
        gender = request.form.get('gender')

        # Generate unique complaint ID first
        count = Complaint.query.count() + 1
        complaint_id = f'CMP-{count:06d}'

        # Handle file upload
        image_path = None
        if 'evidence_file' in request.files:
            file = request.files['evidence_file']
            if file and file.filename and allowed_file(file.filename):
                # Generate unique filename
                ext = file.filename.rsplit('.', 1)[1].lower()
                filename = f"{complaint_id}_{int(datetime.utcnow().timestamp())}.{ext}"
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                image_path = filename

        new_complaint = Complaint(
            complaint_id=complaint_id,
            user_id=current_user.id,
            title=title,
            description=description,
            category=category,
            division=division,
            subdivision=subdivision,
            other_division=other_division if other_division else None,
            other_subdivision=other_subdivision if other_subdivision else None,
            location=location,
            latitude=float(latitude) if latitude else None,
            longitude=float(longitude) if longitude else None,
            image_path=image_path,
            age=int(age) if age else None,
            gender=gender if gender else None
        )

        db.session.add(new_complaint)
        db.session.commit()

        flash(f'Complaint submitted successfully! Your Complaint ID is {complaint_id}', 'success')
        return redirect(url_for('citizen_dashboard'))
    
    return render_template('submit_complaint.html')

@app.route('/citizen/track/<complaint_id>')
@login_required
def track_complaint(complaint_id):
    if current_user.role != 'citizen':
        return redirect(url_for('home'))
    
    complaint = Complaint.query.filter_by(complaint_id=complaint_id, user_id=current_user.id).first()
    if not complaint:
        flash('Complaint not found', 'error')
        return redirect(url_for('citizen_dashboard'))
    
    return render_template('track_complaint.html', complaint=complaint)

@app.route('/citizen/feedback/<complaint_id>', methods=['GET', 'POST'])
@login_required
def give_feedback(complaint_id):
    if current_user.role != 'citizen':
        return redirect(url_for('home'))
    
    complaint = Complaint.query.filter_by(complaint_id=complaint_id, user_id=current_user.id).first()
    if not complaint:
        flash('Complaint not found', 'error')
        return redirect(url_for('citizen_dashboard'))
    
    if complaint.status != 'Resolved':
        flash('Feedback can only be given for resolved complaints', 'error')
        return redirect(url_for('citizen_dashboard'))
    
    existing_feedback = Feedback.query.filter_by(complaint_id=complaint.id).first()
    
    if request.method == 'POST':
        rating = request.form.get('rating')
        feedback_text = request.form.get('feedback_text')
        
        if existing_feedback:
            existing_feedback.rating = rating
            existing_feedback.feedback_text = feedback_text
        else:
            new_feedback = Feedback(complaint_id=complaint.id, rating=rating, feedback_text=feedback_text)
            db.session.add(new_feedback)
        
        db.session.commit()
        flash('Thank you for your feedback!', 'success')
        return redirect(url_for('citizen_dashboard'))
    
    return render_template('feedback.html', complaint=complaint, feedback=existing_feedback)

# Official Routes
@app.route('/official/dashboard')
@login_required
def official_dashboard():
    if current_user.role != 'official':
        return redirect(url_for('home'))
    
    complaints = Complaint.query.filter_by(assigned_to=current_user.id).order_by(Complaint.created_at.desc()).all()
    return render_template('official_dashboard.html', complaints=complaints)

@app.route('/official/update/<complaint_id>', methods=['GET', 'POST'])
@login_required
def update_complaint(complaint_id):
    if current_user.role != 'official':
        return redirect(url_for('home'))
    
    complaint = Complaint.query.filter_by(complaint_id=complaint_id, assigned_to=current_user.id).first()
    if not complaint:
        flash('Complaint not found or not assigned to you', 'error')
        return redirect(url_for('official_dashboard'))
    
    if request.method == 'POST':
        status = request.form.get('status')
        remarks = request.form.get('remarks')
        
        complaint.status = status
        complaint.remarks = remarks
        complaint.updated_at = datetime.utcnow()
        
        # Handle official file upload
        if 'official_evidence_file' in request.files:
            file = request.files['official_evidence_file']
            if file and file.filename and allowed_file(file.filename):
                # Generate unique filename with official prefix
                ext = file.filename.rsplit('.', 1)[1].lower()
                filename = f"official_{complaint.complaint_id}_{int(datetime.utcnow().timestamp())}.{ext}"
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                complaint.official_image_path = filename
        
        db.session.commit()
        
        flash('Complaint updated successfully!', 'success')
        return redirect(url_for('official_dashboard'))
    
    return render_template('update_complaint.html', complaint=complaint)

# Admin Routes
@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    if current_user.role != 'admin':
        return redirect(url_for('home'))
    
    total_complaints = Complaint.query.count()
    pending_complaints = Complaint.query.filter(Complaint.status.in_(['Submitted', 'Under Review'])).count()
    resolved_complaints = Complaint.query.filter_by(status='Resolved').count()
    in_progress = Complaint.query.filter(Complaint.status.in_(['Assigned', 'In Progress'])).count()
    
    recent_complaints = Complaint.query.order_by(Complaint.created_at.desc()).limit(10).all()
    officials = User.query.filter_by(role='official').all()
    
    return render_template('admin_dashboard.html', 
                         total=total_complaints, 
                         pending=pending_complaints,
                         resolved=resolved_complaints,
                         in_progress=in_progress,
                         complaints=recent_complaints,
                         officials=officials)

@app.route('/admin/assign/<complaint_id>', methods=['GET', 'POST'])
@login_required
def assign_complaint(complaint_id):
    if current_user.role != 'admin':
        return redirect(url_for('home'))
    
    complaint = Complaint.query.filter_by(complaint_id=complaint_id).first()
    if not complaint:
        flash('Complaint not found', 'error')
        return redirect(url_for('admin_dashboard'))
    
    officials = User.query.filter_by(role='official').all()
    
    if request.method == 'POST':
        official_id = request.form.get('official_id')
        
        complaint.assigned_to = official_id
        complaint.status = 'Assigned'
        complaint.updated_at = datetime.utcnow()
        
        # Handle admin file upload
        if 'admin_evidence_file' in request.files:
            file = request.files['admin_evidence_file']
            if file and file.filename and allowed_file(file.filename):
                # Generate unique filename with admin prefix
                ext = file.filename.rsplit('.', 1)[1].lower()
                filename = f"admin_{complaint.complaint_id}_{int(datetime.utcnow().timestamp())}.{ext}"
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                complaint.admin_image_path = filename
        
        db.session.commit()
        
        flash('Complaint assigned successfully!', 'success')
        return redirect(url_for('admin_dashboard'))
    
    return render_template('assign_complaint.html', complaint=complaint, officials=officials)

@app.route('/admin/officials', methods=['GET', 'POST'])
@login_required
def manage_officials():
    if current_user.role != 'admin':
        return redirect(url_for('home'))
    
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        password = request.form.get('password')
        department = request.form.get('department')
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered', 'error')
            return redirect(url_for('manage_officials'))
        
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_official = User(name=name, email=email, phone=phone,
                           password=hashed_password, role='official', department=department)
        db.session.add(new_official)
        db.session.commit()
        
        flash('Official added successfully!', 'success')
        return redirect(url_for('manage_officials'))
    
    officials = User.query.filter_by(role='official').all()
    return render_template('manage_officials.html', officials=officials)

@app.route('/admin/reports')
@login_required
def reports():
    if current_user.role != 'admin':
        return redirect(url_for('home'))
    
    # Category-wise statistics
    categories = db.session.query(
        Complaint.category,
        db.func.count(Complaint.id).label('count')
    ).group_by(Complaint.category).all()
    
    # Status-wise statistics
    statuses = db.session.query(
        Complaint.status,
        db.func.count(Complaint.id).label('count')
    ).group_by(Complaint.status).all()
    
    # Monthly statistics
    monthly = db.session.query(
        db.func.strftime('%Y-%m', Complaint.created_at).label('month'),
        db.func.count(Complaint.id).label('count')
    ).group_by('month').order_by('month').limit(12).all()
    
    return render_template('reports.html', categories=categories, statuses=statuses, monthly=monthly)

# API Routes
@app.route('/api/complaints')
def api_complaints():
    complaints = Complaint.query.order_by(Complaint.created_at.desc()).all()
    return jsonify([{
        'complaint_id': c.complaint_id,
        'title': c.title,
        'category': c.category,
        'status': c.status,
        'location': c.location,
        'created_at': c.created_at.isoformat()
    } for c in complaints])

@app.route('/api/stats')
def api_stats():
    total = Complaint.query.count()
    resolved = Complaint.query.filter_by(status='Resolved').count()
    pending = total - resolved
    
    return jsonify({'total': total, 'resolved': resolved, 'pending': pending})

# Initialize Database
def init_db():
    with app.app_context():
        db.create_all()
        
        # Create default admin if not exists
        admin = User.query.filter_by(email='admin@cgmp.gov').first()
        if not admin:
            admin = User(
                name='Administrator',
                email='admin@cgmp.gov',
                phone='1234567890',
                password=generate_password_hash('admin123', method='pbkdf2:sha256'),
                role='admin',
                department='Administration'
            )
            db.session.add(admin)
            db.session.commit()
            print("Default admin created: admin@cgmp.gov / admin123")

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5000)


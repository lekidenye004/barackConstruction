from flask import Flask, render_template, request, jsonify, flash, redirect, url_for
from flask_mail import Mail, Message
from datetime import datetime

app = Flask(__name__)

# ========== EMAIL CONFIGURATION ==========
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'josephkidenye@gmail.com'
app.config['MAIL_PASSWORD'] = 'fasq rpzf rzsn eeve'  # Your app password
app.config['MAIL_DEFAULT_SENDER'] = 'josephkidenye@gmail.com'

# Initialize Mail
mail = Mail(app)


# ========== YOUR EXISTING ROUTES ==========
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/services')
def services():
    return render_template('service.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/quote')
def quote():
    return render_template('quote.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/projects')
def projects():
    return render_template('project.html')


# ========== QUOTE SUBMISSION ROUTE ==========
@app.route('/submit-quote', methods=['POST'])
def submit_quote():
    try:
        # Get all form data
        service_type = request.form.get('service_type')
        start_date = request.form.get('start_date')
        completion_date = request.form.get('completion_date')
        project_description = request.form.get('project_description')
        budget = request.form.get('budget')
        property_size = request.form.get('property_size')
        rooms = request.form.get('rooms')
        location = request.form.get('location')
        features = request.form.getlist('features')
        special_requirements = request.form.get('special_requirements')
        full_name = request.form.get('full_name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        alt_phone = request.form.get('alt_phone')
        contact_method = request.form.get('contact_method')
        contact_time = request.form.get('contact_time')
        referral_source = request.form.get('referral_source')

        # Format budget
        budget_text = f"KES {int(budget):,}" if budget else 'Not specified'

        # Create email body
        email_body = f"""
        NEW QUOTE REQUEST - Premium Constructions
        {'=' * 50}

        SUBMISSION TIME: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

        {'=' * 50}
        SERVICE INFORMATION
        {'=' * 50}
        Service Type: {service_type}
        Start Date: {start_date if start_date else 'Not specified'}
        Completion Date: {completion_date if completion_date else 'Not specified'}

        {'=' * 50}
        PROJECT DETAILS
        {'=' * 50}
        Description: {project_description}
        Budget: {budget_text}
        Property Size: {property_size} sq m if property_size else 'Not specified'
        Rooms/Floors: {rooms if rooms else 'Not specified'}
        Location: {location if location else 'Not specified'}
        Additional Features: {', '.join(features) if features else 'None'}
        Special Requirements: {special_requirements if special_requirements else 'None'}

        {'=' * 50}
        CLIENT INFORMATION
        {'=' * 50}
        Full Name: {full_name}
        Email: {email}
        Phone: {phone}
        Alternate Phone: {alt_phone if alt_phone else 'Not provided'}
        Preferred Contact: {contact_method}
        Best Contact Time: {contact_time}
        Referral Source: {referral_source if referral_source else 'Not specified'}

        {'=' * 50}
        ACTION REQUIRED
        {'=' * 50}
        Please contact the client within 24 hours to provide a detailed quote.
        Client prefers to be contacted via: {contact_method}
        """

        # Send email to josephkidenye@gmail.com
        msg = Message(
            subject=f"NEW QUOTE: {full_name} - {service_type}",
            recipients=['josephkidenye@gmail.com'],
            body=email_body
        )
        mail.send(msg)
        print(f"✅ Quote email sent to josephkidenye@gmail.com")

        # Send confirmation email to client
        client_msg = Message(
            subject="Thank you for your quote request - Premium Constructions",
            recipients=[email],
            body=f"""
Dear {full_name},

Thank you for requesting a quote from Premium Constructions!

We have received your request and our team will contact you within 24 hours to discuss your project in detail.

📋 YOUR REQUEST SUMMARY:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Service Type: {service_type}
Project: {project_description[:150]}...
Location: {location if location else 'Not specified'}
Budget Range: {budget_text}

📞 CONTACT DETAILS:
We will contact you via: {contact_method}
Best time: {contact_time}

WHAT HAPPENS NEXT?
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. Our team will review your requirements
2. We'll contact you within 24 hours
3. We'll schedule a site visit if needed
4. You'll receive a detailed quote

If you have any urgent questions, please contact us:
📞 Phone: +254 700 057910
📧 Email: josephkidenye@.com
🌐 Website: www.premiumconstructions.com

Thank you for choosing Premium Constructions!

Best regards,
Premium Constructions Team
Building Excellence Since 2010
            """
        )
        mail.send(client_msg)
        print(f"✅ Confirmation email sent to {email}")

        return jsonify({
            'success': True,
            'message': 'Quote submitted successfully! Check your email for confirmation.'
        })

    except Exception as e:
        print(f" Error sending email: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500





if __name__ == '__main__':
    app.run(debug=True)

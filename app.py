from flask import Flask, render_template, request, redirect, session, send_file
from werkzeug.utils import secure_filename
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph
import os
import db

app = Flask(__name__)
app.secret_key = "food_rescue_connect"

UPLOAD_FOLDER = "static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


# ---------------- HOME ---------------- #

@app.route("/")
def home():
    return render_template("index.html")


# ---------------- REGISTER ---------------- #

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        fullname = request.form["fullname"]
        email = request.form["email"]
        password = request.form["password"]
        phone = request.form["phone"]
        role = request.form["role"]

        query = """
        INSERT INTO users (full_name, email, password, phone, role)
        VALUES (%s, %s, %s, %s, %s)
        """

        values = (fullname, email, password, phone, role)

        db.cursor.execute(query, values)
        db.connection.commit()

        return "Registration Successful! Data Saved to MySQL"

    return render_template("register.html")


# ---------------- LOGIN ---------------- #

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        query = """
        SELECT * FROM users
        WHERE email=%s AND password=%s
        """

        values = (email, password)

        db.cursor.execute(query, values)

        user = db.cursor.fetchone()

        if user:
            session["user_id"] = user[0]
            session["role"] = user[5]
            session["full_name"]=user[1]


            role = user[5]

            if role == "Donor":
                return render_template("donor_dashboard.html")

            elif role == "NGO":
                return render_template("ngo_dashboard.html")

            elif role == "Admin":
                return render_template("admin_dashboard.html")

        else:
            return "Invalid Email or Password"

    return render_template("login.html")


# ---------------- DONATE FOOD ---------------- #

@app.route("/donate", methods=["GET", "POST"])
def donate():

    if request.method == "POST":

        food_name = request.form["food_name"]
        quantity = request.form["quantity"]
        expiry_time = request.form["expiry_time"]
        pickup_address = request.form["pickup_address"]
        food_image = request.files["food_image"]

        filename = secure_filename(food_image.filename)

        food_image.save(
            os.path.join(app.config["UPLOAD_FOLDER"], filename)
        )

        query = """
        INSERT INTO food_donations
        (donor_id, food_name, quantity, expiry_time, pickup_address, food_image)
        VALUES (%s, %s, %s, %s, %s, %s)
        """

        donor_id = session["user_id"]

        values = (
            donor_id,
            food_name,
            quantity,
            expiry_time,
            pickup_address,
            filename
        )

        # Save donation
        db.cursor.execute(query, values)
        db.connection.commit()

        # Give 10 reward points
        query = """
        UPDATE users
        SET reward_points = reward_points + 10
        WHERE user_id = %s
        """

        db.cursor.execute(query, (session["user_id"],))
        db.connection.commit()

        # Get reward points and current badge
        query = """
        SELECT reward_points, badge
        FROM users
        WHERE user_id = %s
        """

        db.cursor.execute(query, (session["user_id"],))
        user = db.cursor.fetchone()

        points = user[0]
        current_badge = user[1]

        # Decide new badge
        if points >= 200:
            badge = "👑 Platinum Donor"

        elif points >= 100:
            badge = "🥇 Gold Donor"

        elif points >= 50:
            badge = "🥈 Silver Donor"

        else:
            badge = "🥉 Bronze Donor"

        # Show congratulation only if badge changed
        if current_badge != badge:
            flash(f"🎉 Congratulations! You are now a {badge}.", "success")

        # Update badge
        query = """
        UPDATE users
        SET badge = %s
        WHERE user_id = %s
        """

        db.cursor.execute(query, (badge, session["user_id"]))
        db.connection.commit()

        # Donation success message
        flash("🎉 Food donated successfully! +10 Reward Points earned.", "success")

        return redirect(url_for("donor_dashboard"))

    return render_template("donate_food.html")
@app.route("/view_donations")
def view_donations():

    search = request.args.get("search")
    status = request.args.get("status")

    query = """
    SELECT food_donations.*, users.full_name
    FROM food_donations
    JOIN users
    ON food_donations.donor_id = users.user_id
    WHERE 1=1
    """

    values = []

    if search:
        query += """
        AND (
            food_name LIKE %s
            OR users.full_name LIKE %s
            OR status LIKE %s
        )
        """
        search_value = "%" + search + "%"
        values.extend([search_value, search_value, search_value])

    if status:
        query += " AND status=%s"
        values.append(status)

    query += " ORDER BY donation_id DESC"

    db.cursor.execute(query, tuple(values))

    donations = db.cursor.fetchall()

    return render_template(
        "view_donations.html",
        donations=donations
    )
@app.route("/view_users")
def view_users():

    search = request.args.get("search")

    if search:

        query = """
        SELECT *
        FROM users
        WHERE full_name LIKE %s
        OR email LIKE %s
        """

        search_value = "%" + search + "%"

        db.cursor.execute(query, (search_value, search_value))

    else:

        query = "SELECT * FROM users"

        db.cursor.execute(query)

    users = db.cursor.fetchall()

    return render_template(
        "view_users.html",
        users=users
    )

@app.route("/delete_user/<int:user_id>")
def delete_user(user_id):

    query = "DELETE FROM users WHERE user_id = %s"

    db.cursor.execute(query, (user_id,))
    db.connection.commit()

    return redirect("/view_users")

@app.route("/logout")
def logout():

    session.clear()

    return redirect("/")


@app.route("/my_donations")
def my_donations():

    donor_id = session["user_id"]

    status = request.args.get("status")

    if status:

        query = """
        SELECT donation_id,
               food_name,
               quantity,
               expiry_time,
               pickup_address,
               status,
               food_image
        FROM food_donations
        WHERE donor_id = %s
        AND status = %s
        """

        db.cursor.execute(query, (donor_id, status))

    else:

        query = """
        SELECT donation_id,
               food_name,
               quantity,
               expiry_time,
               pickup_address,
               status,
               food_image
        FROM food_donations
        WHERE donor_id = %s
        """

        db.cursor.execute(query, (donor_id,))

    donations = db.cursor.fetchall()

    return render_template(
        "my_donations.html",
        donations=donations
    )

@app.route("/available_donations")
def available_donations():

    query = """
    SELECT *
    FROM food_donations
    WHERE status='Available'
    """

    db.cursor.execute(query)

    donations = db.cursor.fetchall()

    return render_template(
        "available_donations.html",
        donations=donations
    )

@app.route("/accepted_donations")
def accepted_donations():

    query = """
    SELECT *
    FROM food_donations
    WHERE status='Accepted'
    """

    db.cursor.execute(query)

    donations = db.cursor.fetchall()

    return render_template(
        "accepted_donations.html",
        donations=donations
    )

@app.route("/completed_donations")
def completed_donations():

    query = """
    SELECT *
    FROM food_donations
    WHERE status='Completed'
    """

    db.cursor.execute(query)

    donations = db.cursor.fetchall()

    return render_template(
        "completed_donations.html",
        donations=donations
    )
@app.route("/accept_donation/<int:donation_id>")
def accept_donation(donation_id):

    query = """
        UPDATE food_donations
        SET status = 'Accepted'
        WHERE donation_id = %s
    """

    db.cursor.execute(query, (donation_id,))
    db.connection.commit()

    return redirect("/available_donations")

#donar dashboard
@app.route("/donor_dashboard")
def donor_dashboard():

    query = """
    SELECT reward_points, badge
    FROM users
    WHERE user_id = %s
    """

    db.cursor.execute(query, (session["user_id"],))
    user = db.cursor.fetchone()

    reward_points = user[0]
    badge = user[1]

    return render_template(
        "donor_dashboard.html",
        full_name=session["full_name"],
        reward_points=reward_points,
        badge=badge
    )
    


@app.route("/ngo_dashboard")
def ngo_dashboard():
    return render_template(
    "ngo_dashboard.html",
     full_name=session["full_name"]
    )

@app.route("/admin_dashboard")
def admin_dashboard():

    # Total Users
    db.cursor.execute("SELECT COUNT(*) FROM users")
    total_users = db.cursor.fetchone()[0]

    # Total Donations
    db.cursor.execute("SELECT COUNT(*) FROM food_donations")
    total_donations = db.cursor.fetchone()[0]

    # Available Donations
    db.cursor.execute(
        "SELECT COUNT(*) FROM food_donations WHERE status='Available'"
    )
    available = db.cursor.fetchone()[0]

    # Accepted Donations
    db.cursor.execute(
        "SELECT COUNT(*) FROM food_donations WHERE status='Accepted'"
    )
    accepted = db.cursor.fetchone()[0]

    # Completed Donations
    db.cursor.execute(
        "SELECT COUNT(*) FROM food_donations WHERE status='Completed'"
    )
    completed = db.cursor.fetchone()[0]

    # Recent Donations
    query = """
    SELECT food_name, status
    FROM food_donations
    ORDER BY donation_id DESC
    LIMIT 5
    """

    db.cursor.execute(query)
    recent_donations = db.cursor.fetchall()

    return render_template(
        "admin_dashboard.html",
        full_name=session["full_name"],
        total_users=total_users,
        total_donations=total_donations,
        available=available,
        accepted=accepted,
        completed=completed,
        recent_donations=recent_donations
    )
@app.route("/edit_donation/<int:donation_id>", methods=["GET", "POST"])
def edit_donation(donation_id):

    # GET request - Open Edit Page
    if request.method == "GET":

        query = """
        SELECT donation_id,
               food_name,
               quantity,
               expiry_time,
               pickup_address,
               status
        FROM food_donations
        WHERE donation_id = %s
        """

        db.cursor.execute(query, (donation_id,))

        donation = db.cursor.fetchone()

        return render_template(
            "edit_donation.html",
            donation=donation
        )

    # POST request - Update Donation
    food_name = request.form["food_name"]
    quantity = request.form["quantity"]
    expiry_time = request.form["expiry_time"]
    pickup_address = request.form["pickup_address"]

    query = """
    UPDATE food_donations
    SET food_name=%s,
        quantity=%s,
        expiry_time=%s,
        pickup_address=%s
    WHERE donation_id=%s
    """

    values = (
        food_name,
        quantity,
        expiry_time,
        pickup_address,
        donation_id
    )

    db.cursor.execute(query, values)
    db.connection.commit()

    return redirect("/my_donations")

@app.route("/profile", methods=["GET", "POST"])
def profile():

    user_id = session["user_id"]

    if request.method == "POST":

        full_name = request.form["full_name"]
        phone = request.form["phone"]

        query = """
        UPDATE users
        SET full_name=%s,
            phone=%s
        WHERE user_id=%s
        """

        db.cursor.execute(query, (full_name, phone, user_id))
        db.connection.commit()

        # Update session name
        session["full_name"] = full_name

    query = """
    SELECT *
    FROM users
    WHERE user_id=%s
    """

    db.cursor.execute(query, (user_id,))
    user = db.cursor.fetchone()

    return render_template(
        "profile.html",
        user=user
    )

@app.route("/change_password", methods=["GET", "POST"])
def change_password():

    user_id = session["user_id"]

    if request.method == "POST":

        current_password = request.form["current_password"]
        new_password = request.form["new_password"]
        confirm_password = request.form["confirm_password"]

        # Get current password from database
        query = """
        SELECT password
        FROM users
        WHERE user_id=%s
        """

        db.cursor.execute(query, (user_id,))
        user = db.cursor.fetchone()

        # Check current password
        if user[0] != current_password:
            return "❌ Current password is incorrect."

        # Check new password matches confirm password
        if new_password != confirm_password:
            return "❌ New passwords do not match."

        # Update password
        query = """
        UPDATE users
        SET password=%s
        WHERE user_id=%s
        """

        db.cursor.execute(query, (new_password, user_id))
        db.connection.commit()

        return "✅ Password changed successfully."

    return render_template("change_password.html")

@app.route("/complete_donation/<int:donation_id>")
def complete_donation(donation_id):

    query = """
    UPDATE food_donations
    SET status='Completed'
    WHERE donation_id=%s
    """

    db.cursor.execute(query, (donation_id,))
    db.connection.commit()

    return redirect("/accepted_donations")

from flask import Flask, render_template, request, redirect, session, send_file

@app.route("/download_report")
def download_report():

    # Fetch all donations
    query = """
    SELECT donation_id,
           food_name,
           quantity,
           status
    FROM food_donations
    ORDER BY donation_id
    """

    db.cursor.execute(query)
    donations = db.cursor.fetchall()

    # Create PDF
    pdf_file = "donation_report.pdf"

    doc = SimpleDocTemplate(pdf_file)
    elements = []

    styles = getSampleStyleSheet()

    title = Paragraph("<b>Food Rescue Connect - Donation Report</b>", styles["Heading1"])
    elements.append(title)

    data = [["ID", "Food Name", "Quantity", "Status"]]

    for donation in donations:
        data.append([
            str(donation[0]),
            donation[1],
            str(donation[2]),
            donation[3]
        ])

    table = Table(data)

    table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.green),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('GRID', (0,0), (-1,-1), 1, colors.black),
        ('BACKGROUND', (0,1), (-1,-1), colors.beige),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('BOTTOMPADDING', (0,0), (-1,0), 10),
    ]))

    elements.append(table)

    doc.build(elements)

    return send_file(pdf_file, as_attachment=True)

@app.route("/leaderboard")
def leaderboard():

    query = """
    SELECT full_name, reward_points, badge
    FROM users
    WHERE role = 'Donor'
    ORDER BY reward_points DESC
    LIMIT 10
    """

    db.cursor.execute(query)
    donors = db.cursor.fetchall()

    return render_template(
        "leaderboard.html",
        donors=donors
    )

from flask import send_file
from reportlab.pdfgen import canvas
import os

@app.route("/download_certificate")
def download_certificate():

    query = """
    SELECT full_name, reward_points, badge
    FROM users
    WHERE user_id = %s
    """

    db.cursor.execute(query, (session["user_id"],))
    user = db.cursor.fetchone()

    full_name = user[0]
    reward_points = user[1]
    badge = user[2]

    # Allow certificate only if donor has at least 50 points
    if reward_points < 50:
        return """
        <h2 style='text-align:center;color:red;margin-top:100px;'>
            You need at least <b>50 Reward Points</b>
            to download your certificate.
        </h2>
        """

    filename = "certificate.pdf"

    c = canvas.Canvas(filename)

    c.setFont("Helvetica-Bold", 22)
    c.drawCentredString(300, 780, "FOOD RESCUE CONNECT")

    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(300, 740, "CERTIFICATE OF APPRECIATION")

    c.setFont("Helvetica", 14)
    c.drawCentredString(300, 690, "This Certificate is Proudly Presented To")

    c.setFont("Helvetica-Bold", 20)
    c.drawCentredString(300, 650, full_name)

    c.setFont("Helvetica", 14)
    c.drawCentredString(
        300,
        610,
        "For contributing to reducing food waste"
    )

    c.drawCentredString(
        300,
        590,
        "and helping people in need."
    )

    c.drawString(150, 520, f"Reward Points : {reward_points}")
    c.drawString(150, 490, f"Badge : {badge}")

    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(
        300,
        420,
        "Thank You For Your Contribution!"
    )

    c.drawCentredString(
        300,
        380,
        "Food Rescue Connect Team"
    )

    c.save()

    return send_file(
        filename,
        as_attachment=True
    )
# ---------------- RUN APPLICATION ---------------- #

if __name__ == "__main__":
    app.run(debug=True)
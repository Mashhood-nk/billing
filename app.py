from flask import Flask, render_template, request, send_file
from fpdf import FPDF
import os

app = Flask(__name__)
UPLOAD_FOLDER = "invoices"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def generate_pdf(invoice_data, filename):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(200, 10, "QUOTATION", ln=True, align="C")
    pdf.ln(10)
    
    pdf.set_font("Arial", "", 12)
    pdf.cell(200, 10, "IQAMA", ln=True, align="C")
    pdf.cell(200, 10, "Vengara", ln=True, align="C")
    pdf.cell(200, 10, "Ph: 987186667", ln=True, align="C")
    pdf.ln(10)
    
    pdf.cell(100, 10, f"Quotation No: {invoice_data['quotation_no']}")
    pdf.cell(100, 10, f"Date: {invoice_data['date']}", ln=True)
    pdf.ln(5)
    
    pdf.cell(200, 10, f"Customer: {invoice_data['customer_name']}", ln=True)
    pdf.cell(200, 10, f"Phone: {invoice_data['customer_phone']}", ln=True)
    pdf.ln(10)
    
    pdf.set_font("Arial", "B", 10)
    pdf.cell(10, 10, "SL", 1)
    pdf.cell(80, 10, "Item Name", 1)
    pdf.cell(30, 10, "Qty", 1)
    pdf.cell(30, 10, "Rate", 1)
    pdf.cell(40, 10, "Total", 1, ln=True)
    
    pdf.set_font("Arial", "", 10)
    total_amount = 0
    for idx, item in enumerate(invoice_data['items'], start=1):
        total = item['qty'] * item['rate']
        total_amount += total
        pdf.cell(10, 10, str(idx), 1)
        pdf.cell(80, 10, item['name'], 1)
        pdf.cell(30, 10, str(item['qty']), 1)
        pdf.cell(30, 10, f"{item['rate']:.2f}", 1)
        pdf.cell(40, 10, f"{total:.2f}", 1, ln=True)
    
    pdf.set_font("Arial", "B", 12)
    pdf.cell(150, 10, "TOTAL", 1)
    pdf.cell(40, 10, f"{total_amount:.2f}", 1, ln=True)
    
    pdf.ln(10)
    pdf.cell(200, 10, "Happy to serve", ln=True)

    
    pdf.output(os.path.join(UPLOAD_FOLDER, filename))

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        customer_name = request.form["customer_name"]
        customer_phone = request.form["customer_phone"]
        quotation_no = request.form["quotation_no"]
        date = request.form["date"]
        
        items = []
        for i in range(len(request.form.getlist("item_name"))):
            items.append({
                "name": request.form.getlist("item_name")[i],
                "qty": int(request.form.getlist("qty")[i]),
                "rate": float(request.form.getlist("rate")[i])
            })
        
        invoice_data = {
            "customer_name": customer_name,
            "customer_phone": customer_phone,
            "quotation_no": quotation_no,
            "date": date,
            "items": items
        }
        filename = f"quotation_{quotation_no}.pdf"
        generate_pdf(invoice_data, filename)
        
        return send_file(os.path.join(UPLOAD_FOLDER, filename), as_attachment=True)
    
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)

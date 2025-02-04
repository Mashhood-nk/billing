from flask import Flask, render_template, request, send_file
from fpdf import FPDF
import os
from num2words import num2words

app = Flask(__name__)
UPLOAD_FOLDER = "invoices"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def generate_pdf(invoice_data, filename):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "INVOICE", ln=True, align="C")
    pdf.ln(10)
    
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 10, invoice_data['company_name'], ln=True, align="C")
    pdf.cell(0, 10, invoice_data['company_address'], ln=True, align="C")
    pdf.cell(0, 10, f"GSTIN: {invoice_data['gstin']}", ln=True, align="C")
    pdf.ln(10)
    
    pdf.cell(100, 10, f"Invoice No: {invoice_data['invoice_no']}")
    pdf.cell(90, 10, f"Date: {invoice_data['date']}", ln=True)
    pdf.ln(5)
    
    pdf.cell(0, 10, f"Customer: {invoice_data['customer_name']}", ln=True)
    pdf.cell(0, 10, f"Phone: {invoice_data['customer_phone']}", ln=True)
    pdf.ln(10)
    
    pdf.set_font("Arial", "B", 10)
    pdf.cell(10, 10, "SL", 1, align="C")
    pdf.cell(77, 10, "Item Name", 1, align="C")
    pdf.cell(25, 10, "Qty", 1, align="C")
    pdf.cell(27, 10, "Rate", 1, align="C")
    pdf.cell(27, 10, "Tax", 1, align="C")
    pdf.cell(27, 10, "Total", 1, ln=True, align="C")
    
    pdf.set_font("Arial", "", 10)
    total_amount = 0
    tax_rate = invoice_data['tax_rate'] / 100
    for idx, item in enumerate(invoice_data['items'], start=1):
        item_total = item['qty'] * item['rate']
        tax_amount = item_total * tax_rate
        total_with_tax = item_total + tax_amount
        total_amount += total_with_tax
        
        pdf.cell(10, 10, str(idx), 1, align="C")
        pdf.cell(77, 10, item['name'], 1, align="C")
        pdf.cell(25, 10, str(item['qty']), 1, align="C")
        pdf.cell(27, 10, f"{item['rate']:.2f}", 1, align="C")
        pdf.cell(27, 10, f"{tax_amount:.2f}", 1, align="C")
        pdf.cell(27, 10, f"{total_with_tax:.2f}", 1, ln=True, align="C")
    
    pdf.set_font("Arial", "B", 12)
    pdf.cell(150, 10, "TOTAL", 1, align="C")
    pdf.cell(43, 10, f"{total_amount:.2f}", 1, ln=True, align="C")
    
    if invoice_data['discount']:
        total_amount -= invoice_data['discount']
        pdf.cell(150, 10, "DISCOUNT", 1, align="C")
        pdf.cell(43, 10, f"-{invoice_data['discount']:.2f}", 1, ln=True, align="C")
    
    pdf.cell(150, 10, "GRAND TOTAL", 1, align="C")
    pdf.cell(43, 10, f"{total_amount:.2f}", 1, ln=True, align="C")
    
    pdf.ln(10)
    pdf.cell(0, 10, f"Amount in words: {num2words(total_amount, lang='en').capitalize()} only.", ln=True, align="C")
    
    pdf.output(os.path.join(UPLOAD_FOLDER, filename))

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        invoice_data = {
            "company_name": request.form["company_name"],
            "company_address": request.form["company_address"],
            "customer_name": request.form["customer_name"],
            "customer_phone": request.form["customer_phone"],
            "invoice_no": request.form["invoice_no"],
            "date": request.form["date"],
            "gstin": request.form["gstin"],
            "tax_rate": float(request.form["tax_rate"]),
            "discount": float(request.form.get("discount", "0") or "0"),
            "items": []
        }
        
        for i in range(len(request.form.getlist("item_name"))):
            invoice_data["items"].append({
                "name": request.form.getlist("item_name")[i],
                "qty": int(request.form.getlist("qty")[i]),
                "rate": float(request.form.getlist("rate")[i])
            })
        
        filename = f"invoice_{invoice_data['invoice_no']}.pdf"
        generate_pdf(invoice_data, filename)
        
        return send_file(os.path.join(UPLOAD_FOLDER, filename), as_attachment=True)
    
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)

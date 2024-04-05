from flask import Flask, request, send_file
from flask_cors import CORS
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import io

app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})

@app.route('/generate-pdf', methods=['POST'])
def generate_pdf():
    dados = request.json
    pdf_buffer = io.BytesIO()
    c = canvas.Canvas(pdf_buffer, pagesize=letter)
    width, height = letter
    c.setFont("Helvetica-Bold", 12)
    c.drawString(100, height - 100, "Informações do Funcionário")
    c.setFont("Helvetica", 10)
    y_position = height - 130

    for key, value in dados.items():
        if key != "imageUrl":
            c.drawString(100, y_position, f"{key}: {value}")
            y_position -= 20

    # Verifique se 'imageUrl' está presente e atualize y_position conforme necessário
    if 'imageUrl' in dados:
        # Ajuste essa altura com base na altura estimada da imagem
        # Assumindo que você quer manter a largura da imagem em 200 e preservar a proporção,
        # a altura pode ser estimada ou ajustada conforme necessário
        image_height_estimate = 150  # Ajuste conforme necessário
        new_y_position = y_position - image_height_estimate - 20  # Ajustar margem

        try:
            image = ImageReader(dados['imageUrl'])
            # Aqui, usamos new_y_position em vez de y_position - 100
            c.drawImage(image, 100, new_y_position, width=200, preserveAspectRatio=True, mask='auto')
        except Exception as e:
            print(f"Erro ao carregar a imagem: {e}")

    c.save()
    pdf_buffer.seek(0)

    return send_file(pdf_buffer, as_attachment=True, download_name='informacoes_funcionario.pdf', mimetype='application/pdf')

if __name__ == '__main__':
    app.run(debug=True)
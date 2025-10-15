
from flask import Flask, render_template, request, send_file, jsonify
import io, csv

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/calculate', methods=['POST'])
def calculate():
    data = request.json or {}
    try:
        instances = int(data.get('instances', 0))
        vcpu = int(data.get('vcpu', 0))
        hours = float(data.get('hours', 0))
        price_vcpu = float(data.get('price_vcpu', 0))
        storage = float(data.get('storage', 0))
        price_storage = float(data.get('price_storage', 0))
        bandwidth = float(data.get('bandwidth', 0))
        price_bandwidth = float(data.get('price_bandwidth', 0))
    except Exception as e:
        return jsonify({'error': 'invalid input', 'details': str(e)}), 400

    computeCost = instances * vcpu * hours * price_vcpu
    storageCost = storage * price_storage
    bandwidthCost = bandwidth * price_bandwidth
    total = computeCost + storageCost + bandwidthCost

    return jsonify({
        'computeCost': round(computeCost, 2),
        'storageCost': round(storageCost, 2),
        'bandwidthCost': round(bandwidthCost, 2),
        'total': round(total, 2)
    })

@app.route('/download/csv', methods=['POST'])
def download_csv():
    data = request.json or {}
    instances = int(data.get('instances', 0))
    vcpu = int(data.get('vcpu', 0))
    hours = float(data.get('hours', 0))
    price_vcpu = float(data.get('price_vcpu', 0))
    storage = float(data.get('storage', 0))
    price_storage = float(data.get('price_storage', 0))
    bandwidth = float(data.get('bandwidth', 0))
    price_bandwidth = float(data.get('price_bandwidth', 0))

    computeCost = instances * vcpu * hours * price_vcpu
    storageCost = storage * price_storage
    bandwidthCost = bandwidth * price_bandwidth
    total = computeCost + storageCost + bandwidthCost

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['Provider','Instances','vCPU','Hours','Price_vCPU','Storage_GB','Price_Storage','Bandwidth_GB','Price_Bandwidth','ComputeCost','StorageCost','BandwidthCost','Total'])
    writer.writerow([data.get('provider',''), instances, vcpu, hours, price_vcpu, storage, price_storage, bandwidth, price_bandwidth, computeCost, storageCost, bandwidthCost, total])
    output.seek(0)
    return send_file(
        io.BytesIO(output.getvalue().encode('utf-8')),
        mimetype='text/csv',
        as_attachment=True,
        download_name='cloud_cost_estimate.csv'
    )

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

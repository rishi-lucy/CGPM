<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Assign Complaint - CGMP</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        :root { --primary-color: #2c3e50; --secondary-color: #3498db; }
        body { background: #f8f9fa; }
        .sidebar { min-height: 100vh; background: var(--primary-color); color: white; }
        .sidebar a { color: rgba(255,255,255,0.8); text-decoration: none; padding: 12px 20px; display: block; transition: all 0.3s; }
        .sidebar a:hover, .sidebar a.active { background: rgba(255,255,255,0.1); color: white; }
        .form-card { background: white; border-radius: 15px; padding: 30px; box-shadow: 0 2px 10px rgba(0,0,0,0.05); }
    </style>
</head>
<body>
    <div class="container-fluid">
        <div class="row">
            <div class="col-md-3 sidebar p-0">
                <div class="p-4 text-center"><h4>CGMP</h4><p class="mb-0">Admin Portal</p></div>
                <hr>
                <a href="/admin/dashboard">Dashboard</a>
                <a href="/admin/officials">Manage Officials</a>
                <a href="/logout">Logout</a>
            </div>
            <div class="col-md-9 p-4">
                <div class="mb-4"><a href="/admin/dashboard" class="text-muted">Back to Dashboard</a></div>
                <div class="form-card">
                    <h3 class="mb-4">Assign Complaint</h3>
                    <div class="mb-4 p-3 bg-light rounded">
                        <h5>{{ complaint.title }}</h5>
                        <p class="text-muted mb-0">ID: {{ complaint.complaint_id }} | Category: {{ complaint.category }}</p>
                    </div>
                    <form method="POST">
                        <div class="mb-3">
                            <label class="form-label">Assign to Official</label>
                            <select class="form-select" name="official_id" required>
                                <option value="">Select Official</option>
                                {% for official in officials %}
                                <option value="{{ official.id }}">{{ official.name }} - {{ official.department }}</option>
                                {% endfor %}
                            </select>
                        </div>
                        <button type="submit" class="btn btn-primary">Assign Complaint</button>
                    </form>
                </div>
        </div>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>

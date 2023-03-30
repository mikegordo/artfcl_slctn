<!DOCTYPE html>
<html>
<head>
	<title>Artfct_slctn</title>
	<meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
	<link rel="preconnect" href="https://fonts.googleapis.com">
	<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
	<link href="https://fonts.googleapis.com/css2?family=Roboto+Mono:ital,wght@0,300;0,400;0,600;1,300;1,400;1,600&display=swap" rel="stylesheet">
	<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-aFq/bzH65dt+w6FI2ooMVUpc+21e0SRygnTpmBvdBgSdnuTN7QbdgL+OapgHtvPp" crossorigin="anonymous">
	<link rel="stylesheet" type="text/css" href="static/main.css">
</head>
<body>

	<div class="container">
		<div class="row">
			<div class="col">
				<h2>Artfct_slctn</h2>
			</div>
		</div>

		<div class="row">
			<div class="col-4">
				<div>
					<h4>Jobs</h4>
				</div>
				<div id="job_list"></div>
			</div>

			<div class="col">
				<div><h4><span id="job_id"></span></h4></div>
				<div id="job_info">
				</div>
			</div>
		</div>
	</div>

	<script>
	var jb = '';

	function query_jobs_list() {
		var req = new XMLHttpRequest();
		req.open('GET', '/jobs', true);
		req.onload = function() {
			if (req.status >= 200 && req.status < 400) {
				const resp = JSON.parse(req.responseText);
				populate_jobs_list(resp.jobs);
			}
		};
		req.send();
	}

	function populate_jobs_list(rows) {
		const job_list = document.querySelector('#job_list');
		const div = document.createElement('div');
		for (const [k, t] of Object.entries(rows)) {
			const d = document.createElement('div');
			d.innerHTML = '<a href="javascript:read_job(\'' + k + '\');">' + k + '</a>'
			d.innerHTML += ' <span class="status-' + t.status + '"></span>'
			div.appendChild(d);
		}
		job_list.innerHTML = "";
		job_list.append(div);
	}
	
	function read_job(job_id) {
		var req = new XMLHttpRequest();
		req.open('GET', '/job?job=' + job_id, true);
		req.onload = function() {
			if (req.status >= 200 && req.status < 400) {
				const resp = JSON.parse(req.responseText);
				document.querySelector('#job_id').innerHTML = job_id
				populate_jobs_info(resp.job)
				jb = job_id
			}
		};
		req.send();
	}

	function populate_jobs_info(job) {
		const job_info= document.querySelector('#job_info');
		const table = document.createElement('table');
		table.classList.add("table");
		for (const [k, t] of Object.entries(job)) {
			const tr = document.createElement('tr');
			tr.innerHTML = '<th scope="row">' + k + '</th>' + '<td>' + t + '</td>'
			table.appendChild(tr);
		}

		job_info.innerHTML = "";
		job_info.append(table);
	}

	var idVar = setInterval(() => { 
		query_jobs_list();
	}, 5000);

	query_jobs_list();

	var jbup = setInterval(() => { 
		if (jb != '') {
			read_job(jb)
		}
	}, 1000);

	</script>
</body>
</html>

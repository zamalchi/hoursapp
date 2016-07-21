

<script type="text/javascript">

/*
// come back to this maybe
function focusEndTime(endID) {
	console.log("In focusEndTime()")
	console.log("endID:", endID)
	document.getElementById(endID).focus();
}
*/


function confirmDelete() {
	var choice = confirm("Are you sure you want to delete records?");
	if (choice) {
		document.getElementById("deleteConfirm").value = "true";
	}
}

function emailRecords() {
	confirm("Are you sure you want to email records?");
}


// gets element with provided id, sets value to "", and gives focus
function focusAndClearField(id) {
	var elem = document.getElementById(id);
	elem.value = "";
	elem.focus();
}

// @param recordID: id of record that should stay open
// loops through and closes all of the records; then opens the one specified by recordID
function openForm(recordID) {
	var i = 0
	var form = document.getElementById('record' + i)
	while (form != null) {
		form.classList.remove('in');
		form.classList.add('collapse');
		// get next record
		form = document.getElementById('record' + (++i))
	}
	// set specified record to be open
	var form = document.getElementById(recordID);
	form.classList.remove('collapse');
	form.classList.add('in');
}

function adjustNextIndex(insertID, recordIndex) {
	document.getElementById(insertID).value = recordIndex;
}

function openViewer() {
	var str = document.getElementById("viewRecords").value;
	OpenWindow=window.open("", "newwin", "width=550, height=750, toolbar=no,scrollbars="+scroll+",menubar=no");
	OpenWindow.moveTo(0,0);
	OpenWindow.document.write(`
	<html>
	<head>
		<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/css/bootstrap.min.css"/>
		<link rel="stylesheet" href="http://netdna.bootstrapcdn.com/bootstrap/3.1.1/css/bootstrap.min.css"/>
	 	<link rel="stylesheet" type="text/css" href="{{ url('static', filename='hours.css') }}" />
		<title>Hours</title>
	</head>
	<body>
	<div class="container" id="viewerContents">
		<div class="row">
			<div class="col-md-6 col-md-offset-3">
				<div class="panel panel-default">
					<div class="panel-body">`);
	OpenWindow.document.write(str);
	OpenWindow.document.write(`
					</div>
				</div>
			</div>
		</div>
	</div>
	</body>
	</html>
	`);
	var contents = document.getElementById("viewerContents");
	console.log("width: " + contents.offsetWidth + " height: " + contents.offsetHeight)
	OpenWindow.resizeTo(contents.offsetWidth, contents.offsetHeight);
	OpenWindow.document.close();
	self.name="main"
}

</script>
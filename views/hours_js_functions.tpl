

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
	confirm("Are you sure you want to delete records?");
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


</script>
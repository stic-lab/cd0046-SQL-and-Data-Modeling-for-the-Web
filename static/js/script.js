window.parseISOString = function parseISOString(s) {
  var b = s.split(/\D+/);
  return new Date(Date.UTC(b[0], --b[1], b[2], b[3], b[4], b[5], b[6]));
};


function deleteObj(e) {
  const paramArray = e.id.split("_");
  const url = paramArray[0] + '/' + paramArray[1];
  deleteObj = confirm("Do you really want to delete " + paramArray[0] + " " + paramArray[1])
  if (deleteObj) {
    fetch(paramArray[1], {
      method: 'DELETE'
    })
      .then(response => response.json())
      .then(jsonResponse => {
        console.log(jsonResponse);
        window.location.replace('http://127.0.0.1:5000/' + paramArray[0]);
      })
      .catch(function () {
        console.error('Error occurred');
      })
    
  }
}
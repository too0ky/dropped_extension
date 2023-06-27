async function getCSV() {
  const response = await fetch("http://127.0.0.1:5000/api/documents");
  const jsonData = await response.json();
  console.log(jsonData);

  console.log(jsonData[0])
  console.log(Object.keys(jsonData[0]))

  function jsonToCsv(items) {
    const header = Object.keys(items[0]);
    const headerString = header.join(',');

    // handle null or undefined values here
  const replacer = (key, value) => value ?? '';
  const rowItems = items.map((row) =>
    header
      .map((fieldName) => JSON.stringify(row[fieldName], replacer))
      .join(',')
  );
  // join header and body, and break into separate lines
  const csv = [headerString, ...rowItems].join('\r\n');
  return csv;

 
}

const csv = jsonToCsv(jsonData);
console.log(csv);

const csvBlob = new Blob([jsonData], { type: "text/csv;charset=utf-8" });
const csvUrl = URL.createObjectURL(csvBlob);
console.log(csvUrl);
chrome.downloads.download({
  url: csvUrl,
  saveAs: true
});
}

getCSV()


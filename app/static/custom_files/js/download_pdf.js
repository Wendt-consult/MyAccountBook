$(document).ready(function(){});

function download_pdf() {
    var filename  = 'ThisIsYourPDFFilename.pdf';

    html2canvas($('#invoice_template_body'), {  
        scale: 10,
        onrendered: function (canvas) {
            var canvasImg = canvas.toDataURL("image/png");
            var pdf = new jsPDF('p', 'mm', 'a4');
            pdf.addImage(canvas.toDataURL('image/png'), 'PNG', 0, 0, 211, 298);
            pdf.save(filename);
        }
    });
    
}
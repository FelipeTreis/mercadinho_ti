document.addEventListener("DOMContentLoaded", function () {
    const scanButton = document.getElementById('scan-barcode');
    const viewport = document.getElementById('interactive');

    scanButton.addEventListener('click', function () {
        Quagga.init({
            inputStream: {
                type: "LiveStream",
                constraints: {
                    width: { min: 640 },
                    height: { min: 480 },
                    facingMode: "environment" // Para usar a câmera traseira no celular
                },
                target: viewport
            },
            decoder: {
                readers: ["code_128_reader", "ean_reader", "ean_8_reader", "code_39_reader"]
            }
        }, function (err) {
            if (err) {
                console.log(err);
                return;
            }
            Quagga.start();
        });

        Quagga.onDetected(function (result) {
            const code = result.codeResult.code;
            Quagga.stop();

            // Preenche o campo de pesquisa com o código de barras detectado e submete o formulário
            const searchInput = document.querySelector('input[name="q"]');
            searchInput.value = code;
            searchInput.form.submit();
        });
    });
});    
/**
 * == Fonctions
 */

function getAge(DOB) {
  var today = new Date();
  var birthDate = new Date(DOB);
  var age = today.getFullYear() - birthDate.getFullYear();
  var m = today.getMonth() - birthDate.getMonth();
  if (m < 0 || (m === 0 && today.getDate() < birthDate.getDate())) {
    age--;
  }
  return age;
}

function verifyTicket(scannerResult) {
  scanner.stop();
  const ticketUUID = scannerResult.data;
  fetch(`api/get/${ticketUUID}`)
    .then((data) => data.json())
    .then((data) => {
      if (data == null) {
        Swal.fire({
          title: "Ticket Invalide",
          text: "Ce ticket n'existe pas / n'est pas bon",
          icon: "error",
          confirmButtonText: "Continuer",
        }).then((result) => {
          if (result.isConfirmed) {
            scanner.start();
          }
        });
      } else {
        const icon = data.used == 0 ? "success" : "error";
        const title = data.used == 0 ? "Ticket Valide" : "Ticket Déjà Utilisé";
        // Afficher swall Ticket Valide

        const majeur = getAge(data.anniversaire) >= 18;

        const html = `<div>
          <h3 class="is-size-2" >${data.nom.toUpperCase()} ${data.prenom}</h3>
          <h4 class="is-size-3">${majeur ? "Majeur" : "Mineur"}</h4>
      </div>`;

        Swal.fire({
          title: title,
          html: html,
          icon: icon,
          confirmButtonText: "Continuer",
        }).then((result) => {
          if (result.isConfirmed) {
            scanner.start();
          }
        });
      }
    })
    .catch(() => {
      Swal.fire({
        title: "Ticket Invalide",
        text: "Ce ticket n'existe pas / n'est pas bon",
        icon: "error",
        confirmButtonText: "Continuer",
      }).then((result) => {
        if (result.isConfirmed) {
          scanner.start();
        }
      });
    });
}

/**
 * == Mise en place du Scanner ==
 */
// Récupération des DOM
const video = document.getElementById("qr-video");

// Création du scanner
const scanner = new QrScanner(video, (result) => verifyTicket(result), {
  onDecodeError: (error) => {},
  highlightScanRegion: true,
  highlightCodeOutline: true,
});

scanner.start();

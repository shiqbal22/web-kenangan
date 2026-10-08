// =====================================================================
// script.js -> Bagian interaktif di browser (JavaScript)
// =====================================================================

// ---- 1) Menu titik tiga: buka / tutup ----
const tombolMenu = document.getElementById("menuBtn");
const panelMenu = document.getElementById("menuPanel");

function aturMenu(buka) {
  panelMenu.hidden = !buka;
  tombolMenu.setAttribute("aria-expanded", String(buka));
}
tombolMenu.addEventListener("click", () => aturMenu(panelMenu.hidden));
document.addEventListener("click", (e) => {
  if (!panelMenu.contains(e.target) && e.target !== tombolMenu) aturMenu(false);
});
document.addEventListener("keydown", (e) => { if (e.key === "Escape") aturMenu(false); });

// ---- 2) Efek mengetik di beranda ----
const elKetik = document.getElementById("ketik");
if (elKetik) {
  const daftarTeks = JSON.parse(elKetik.dataset.teks);   // array julukan dari Python
  const kurangGerak = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  let indeksTeks = 0, indeksHuruf = 0, menghapus = false;

  function ketik() {
    const teks = daftarTeks[indeksTeks];
    indeksHuruf += menghapus ? -1 : 1;
    elKetik.textContent = teks.slice(0, indeksHuruf);
    let jeda = menghapus ? 40 : 90;
    if (!menghapus && indeksHuruf === teks.length) { menghapus = true; jeda = 1400; }
    else if (menghapus && indeksHuruf === 0) {
      menghapus = false;
      indeksTeks = (indeksTeks + 1) % daftarTeks.length;
      jeda = 400;
    }
    setTimeout(ketik, jeda);
  }
  if (!kurangGerak) { elKetik.textContent = ""; ketik(); }
}

// ---- 3) Jam digital ----
const elJam = document.getElementById("jam");
if (elJam) {
  function perbaruiJam() {
    const sekarang = new Date();
    elJam.textContent = sekarang.toLocaleDateString("id-ID",
      { weekday: "long", day: "numeric", month: "long", year: "numeric" })
      + " \u00b7 " + sekarang.toLocaleTimeString("id-ID");
  }
  perbaruiJam();
  setInterval(perbaruiJam, 1000);
}

// ---- 4) Pratinjau foto sebelum diupload ----
const inputFoto = document.getElementById("inputFoto");
const kotakPratinjau = document.getElementById("pratinjau");
if (inputFoto) {
  inputFoto.addEventListener("change", () => {
    kotakPratinjau.innerHTML = "";
    for (const file of inputFoto.files) {                  // looping tiap file yang dipilih
      const gambar = document.createElement("img");
      gambar.src = URL.createObjectURL(file);
      kotakPratinjau.appendChild(gambar);
    }
  });
}

// ---- 5) Klik foto untuk memperbesar ----
const lightbox = document.getElementById("lightbox");
if (lightbox) {
  const gambarBesar = lightbox.querySelector("img");
  document.querySelectorAll(".foto-klik").forEach((foto) => {
    foto.addEventListener("click", () => {
      gambarBesar.src = foto.src;
      lightbox.hidden = false;
    });
  });
  lightbox.addEventListener("click", () => { lightbox.hidden = true; });
  document.addEventListener("keydown", (e) => { if (e.key === "Escape") lightbox.hidden = true; });
}

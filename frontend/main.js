import './style.css';
import 'filepond/dist/filepond.min.css'
import * as FilePond from 'filepond';

const TEXT_PATTERNS = [
    "Вероятно, это %1",
    "Полагаю, это %1",
    "Может это %1, а может и нет",
    "Думаю %1, но это не точно",
    "Ставлю сотку, что это %1",
];

window.addEventListener("load", () => {
  const uploader = FilePond.create(
    document.getElementById('uploader')
  );

  uploader.on('addfile', async (error, { file }) => {
    if(error) {
      console.log(error);
      return;
    }
    
    if(!file.type.startsWith("image/")) {
      alert("Эт чё? Мне КАРТИНКУ надо");
      location.reload();
      return;
    }

    // Обойки
    const bg = document.getElementsByClassName('root__preview')[0];
    bg.style.backgroundImage = `url('${URL.createObjectURL(file)}')`;
    bg.style.opacity = 1;

    // Шарики
    const result = document.getElementById('result');
    result.innerText = 'Думаю...';

    const ball = document.getElementsByClassName('app-ball')[0];
    const upl = document.getElementById('uploader');
    ball.style.display = '';
    upl.style.display = 'none';

    // Сама магия
    const formData = new FormData();
    formData.append('image_file', file);

    const response = await fetch('/process', {
      method: "POST",
      body: formData,
    });
    const output = await response.json();

    const pattern = TEXT_PATTERNS[Math.round(Math.random() * TEXT_PATTERNS.length)];
    result.innerText = pattern.replace("%1", output.label);
  })
});

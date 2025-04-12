const $startGameButton = document.querySelector(".start-quiz")
const $questionsContainer = document.querySelector(".questions-container")
const $answersContainer = document.querySelector(".answers-container")
const $questionText = document.querySelector(".question")
const $nextQuestionButton = document.querySelector(".next-question")

$startGameButton.addEventListener("click", startGame)
$nextQuestionButton.addEventListener("click", displayNextQuestions)


let currentQuestionsIndex = 0
let totalCorrect = 0

function startGame(){
    $startGameButton.classList.add("hide")
    $questionsContainer.classList.remove("hide")
    displayNextQuestions()
}

function displayNextQuestions(){
      resetState()

      if(questions.length == currentQuestionsIndex ){
        finishGame()
      }

        $questionText.textContent = questions[currentQuestionsIndex].question
        questions[currentQuestionsIndex].answers.forEach(answer =>{
          const newAnswer = document.createElement("button")
          newAnswer.classList.add("button", "answer")
          newAnswer.textContent = answer.text
          if(answer.correct){
            newAnswer.dataset.correct = answer.correct
          }
          $answersContainer.appendChild(newAnswer)

          newAnswer.addEventListener("click", selectAnswer)
        })
}

function resetState(){
  while($answersContainer.firstChild){
    $answersContainer.removeChild($answersContainer.firstChild)
}

document.body.removeAttribute("class")
$nextQuestionButton.classList.add("hide")
}

function selectAnswer(event) {
    const answerClicked = (event.target)

    if(answerClicked.dataset.correct){
      document.body.classList.add("correct")
      totalCorrect++
    } else {
      document.body.classList.add("incorrect")
    }

    document.querySelectorAll(".answer").forEach(button => {
      if(button.dataset.correct){
        button.classList.add("correct")
      } else {
        button.classList.add("incorrect")
      }

      button.disabled = true
    })

    $nextQuestionButton.classList.remove("hide")
    currentQuestionsIndex++
}


function finishGame(){
  const totalQuestion = questions.length
  const performance = Math.floor(totalCorrect * 100/ totalCorrect)

  let message = ""

  switch(true){
    case(performance >= 90):
      message = "Excelente :)"
      break
    case(performance >= 70):
      message = "muito bom :)"
      break
    case(performance >= 50):
      message = "bom"
      break
    default:
      message = "Pode melhorar :("
  }

 $questionsContainer.innerHTML =
 `
    <p class="final-message">
      Você acertou ${totalCorrect} de ${totalQuestion} questões!]
      <span>Resultado: ${message}</span>
    </p>
    <button onClick =window.location.reload() class="button">
      Refazer teste
    </button>
  `

}





















const questions = [
    {
      question: "Dentro de qual elemento HTML colocamos o JavaScript?",
      answers: [
        { text: "<javascript>", correct: false },
        { text: "<js>", correct: false },
        { text: "<script>", correct: true },
        { text: "<scripting>", correct: false }
      ]
    },
    {
      question: "Onde é o lugar correto para inserir JavaScript?",
      answers: [
        { text: "Tanto no <head> quanto no <body> está correto", correct: true },
        { text: "No <body>", correct: false },
        { text: "No <head>", correct: false },
        { text: "Em outro lugar", correct: false }
      ]
    },
    {
      question: 'Qual é a sintaxe correta para se referir a um script externo chamado "xxx.js"',
      answers: [
        { text: '<script src="xxx.js">', correct: true },
        { text: '<script href="xxx.js">', correct: false },
        { text: '<script name="xxx.js">', correct: false },
        { text: "Nenhuma das alternativas", correct: false }
      ]
    },
    {
      question: 'O arquivo JavaScript externo deve conter a tag <script>',
      answers: [
        { text: "Verdadeiro", correct: false },
        { text: "Falso", correct: true }
      ]
    },
    {
      question: 'Como escrever "Hello World" numa caixa de alerta?',
      answers: [
        { text: 'msg("Hello World");', correct: false },
        { text: 'alert("Hello World");', correct: true },
        { text: 'msgBox("Hello World");', correct: false },
        { text: 'alertBox("Hello World");', correct: false }
      ]
    },
    {
      question: 'Como podemos criar uma função no JavaScript?',
      answers: [
        { text: 'function:myFunction()', correct: false },
        { text: 'function myFunction()', correct: true },
        { text: 'function = myFunction()', correct: false },
        { text: 'Nenhum desses códigos criaria uma função', correct: false }
      ]
    },
    {
      question: 'Como podemos chamar uma função chamada "minhaFuncao"?',
      answers: [
        { text: 'call minhaFuncao()', correct: false },
        { text: 'call function minhaFuncao()', correct: false },
        { text: 'Nenhum desses códigos chamaria essa função', correct: false },
        { text: 'minhaFuncao()', correct: true },
      ]
    },
  ]
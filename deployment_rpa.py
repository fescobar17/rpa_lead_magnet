import streamlit as st
import streamlit.components.v1 as components

# 1. Configurar la página para que aproveche todo el ancho y se vea como una web real
st.set_page_config(layout="wide", page_title="Evaluador de Madurez de Automatización")

# 2. Variable que contendrá todo tu código HTML
codigo_html = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Índice de Madurez de Automatización</title>
    <!-- Tailwind CSS para estilos rápidos y responsivos -->
    <script src="https://cdn.tailwindcss.com"></script>
    <!-- Google Fonts: 'Outfit' para un look muy tecnológico y moderno -->
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&display=swap" rel="stylesheet">
    <!-- Phosphor Icons para iconografía moderna -->
    <script src="https://unpkg.com/@phosphor-icons/web"></script>
    
    <script>
        tailwind.config = {
            theme: {
                extend: {
                    fontFamily: {
                        sans: ['Outfit', 'sans-serif'],
                    },
                    colors: {
                        kruger: {
                            dark: '#0a0f18',
                            darker: '#05080c',
                            cyan: '#00e5ff',
                            orange: '#ff5a00',
                            card: 'rgba(20, 28, 45, 0.7)'
                        }
                    },
                    animation: {
                        'pulse-slow': 'pulse 4s cubic-bezier(0.4, 0, 0.6, 1) infinite',
                        'float': 'float 6s ease-in-out infinite',
                    },
                    keyframes: {
                        float: {
                            '0%, 100%': { transform: 'translateY(0)' },
                            '50%': { transform: 'translateY(-20px)' },
                        }
                    }
                }
            }
        }
    </script>
    <style>
        body {
            background-color: #05080c;
            color: #ffffff;
            overflow-x: hidden;
            /* Patrón de cuadrícula tecnológica de fondo */
            background-image: 
                linear-gradient(rgba(0, 229, 255, 0.03) 1px, transparent 1px),
                linear-gradient(90deg, rgba(0, 229, 255, 0.03) 1px, transparent 1px);
            background-size: 30px 30px;
        }

        /* Esferas de luz de fondo (Efecto neón AI) */
        .bg-glow {
            position: fixed;
            border-radius: 50%;
            filter: blur(100px);
            z-index: -1;
            opacity: 0.4;
        }
        .glow-1 { top: -10%; left: -10%; width: 50vw; height: 50vw; background: radial-gradient(circle, #00e5ff, transparent 70%); }
        .glow-2 { bottom: -10%; right: -10%; width: 40vw; height: 40vw; background: radial-gradient(circle, #ff5a00, transparent 70%); }

        .glass-card {
            background: rgba(15, 23, 42, 0.6);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 255, 255, 0.05);
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
        }

        .option-btn {
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }
        
        .option-btn::before {
            content: '';
            position: absolute;
            top: 0; left: -100%; width: 100%; height: 100%;
            background: linear-gradient(90deg, transparent, rgba(0, 229, 255, 0.1), transparent);
            transition: all 0.4s ease;
        }

        .option-btn:hover::before {
            left: 100%;
        }

        .option-btn:hover {
            border-color: #00e5ff;
            box-shadow: 0 0 15px rgba(0, 229, 255, 0.3);
            transform: translateY(-2px);
        }

        /* Transiciones de pantallas */
        .fade-enter { opacity: 0; transform: scale(0.95) translateY(10px); }
        .fade-enter-active { opacity: 1; transform: scale(1) translateY(0); transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1); }
        .fade-exit { opacity: 1; transform: scale(1) translateY(0); }
        .fade-exit-active { opacity: 0; transform: scale(1.05) translateY(-10px); transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1); }

        .cta-button {
            background: linear-gradient(135deg, #ff5a00 0%, #ff2a00 100%);
            transition: all 0.3s ease;
        }
        .cta-button:hover {
            box-shadow: 0 0 25px rgba(255, 90, 0, 0.6);
            transform: scale(1.05);
        }

        .score-text {
            background: linear-gradient(to right, #00e5ff, #0088ff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-shadow: 0 0 30px rgba(0, 229, 255, 0.4);
        }
    </style>
</head>
<body class="min-h-screen flex flex-col items-center justify-center p-4 relative">

    <!-- Elementos visuales de fondo -->
    <div class="bg-glow glow-1 animate-pulse-slow"></div>
    <div class="bg-glow glow-2 animate-pulse-slow" style="animation-delay: 2s;"></div>

    <!-- PANTALLA DE INICIO -->
    <div id="intro-screen" class="w-full max-w-3xl glass-card rounded-3xl p-8 md:p-12 text-center relative z-10 transition-all duration-500">
        <i class="ph ph-cpu text-6xl text-kruger-cyan mb-6 animate-float inline-block"></i>
        <h1 class="text-4xl md:text-5xl font-extrabold mb-4 tracking-tight">Índice de <span class="text-transparent bg-clip-text bg-gradient-to-r from-kruger-cyan to-blue-500">Automatización</span></h1>
        <p class="text-gray-400 text-lg md:text-xl mb-8">Descubre el nivel de madurez tecnológica de tus procesos en menos de 2 minutos.</p>
        <button onclick="startAssessment()" class="cta-button text-white font-bold py-4 px-10 rounded-full text-lg uppercase tracking-wider inline-flex items-center gap-2">
            Iniciar Diagnóstico <i class="ph-bold ph-arrow-right"></i>
        </button>
    </div>

    <!-- CONTENEDOR DE PREGUNTAS -->
    <div id="quiz-container" class="w-full max-w-3xl hidden relative z-10">
        <!-- Barra de progreso -->
        <div class="mb-8">
            <div class="flex justify-between text-sm text-kruger-cyan font-semibold mb-2">
                <span>Progreso</span>
                <span id="progress-text">0/13</span>
            </div>
            <div class="w-full bg-gray-800 rounded-full h-2">
                <div id="progress-bar" class="bg-gradient-to-r from-kruger-cyan to-blue-500 h-2 rounded-full transition-all duration-500" style="width: 0%"></div>
            </div>
        </div>

        <!-- Tarjeta de Pregunta -->
        <div id="question-card" class="glass-card rounded-3xl p-8 md:p-12 fade-enter-active">
            <h2 id="question-title" class="text-2xl md:text-3xl font-bold mb-8 leading-tight"></h2>
            <div id="options-container" class="space-y-4">
                <!-- Las opciones se inyectan por JS -->
            </div>
        </div>
    </div>

    <!-- PANTALLA DE RESULTADOS -->
    <div id="results-screen" class="w-full max-w-4xl hidden relative z-10 text-center">
        <!-- CTA Superior -->
        <a href="https://fa6g8d848vm.typeform.com/to/fhpptYIr" target="_blank" class="inline-block mb-10 group">
            <div class="px-8 py-4 glass-card border border-kruger-cyan rounded-full text-kruger-cyan font-bold tracking-widest uppercase hover:bg-kruger-cyan hover:text-black transition-all duration-300">
                🚀 Quiero automatizar mis procesos ahora
            </div>
        </a>

        <div class="glass-card rounded-3xl p-10 md:p-16 mb-10 relative overflow-hidden">
            <!-- Deco de circuito en el fondo -->
            <i class="ph ph-circuitry absolute -right-20 -bottom-20 text-[300px] text-white opacity-5"></i>
            
            <h3 class="text-2xl text-gray-400 font-semibold mb-2 uppercase tracking-widest">Score de Madurez</h3>
            <div class="text-8xl md:text-[150px] font-extrabold score-text leading-none my-6" id="final-score">
                0
            </div>
            <div class="text-xl md:text-2xl text-gray-300 font-light max-w-2xl mx-auto" id="result-message">
                Analizando tus datos...
            </div>
        </div>

        <!-- CTA Inferior -->
        <a href="https://fa6g8d848vm.typeform.com/to/fhpptYIr" target="_blank" class="cta-button inline-block text-white font-bold py-5 px-12 rounded-full text-xl uppercase tracking-wider shadow-2xl">
            Hablar con un Especialista AI
        </a>
    </div>

    <script>
        // Data de las preguntas
        const questions = [
            {
                q: "¿Cuánto del proceso depende de copiar y pegar datos entre sistemas?",
                options: ["Casi nada", "Solo en un paso puntual", "En varios momentos", "La mayor parte del proceso", "Proceso completo es puente manual"]
            },
            {
                q: "¿El proceso funciona porque las personas conectan información que los sistemas no conectan solos?",
                options: ["No", "Muy poco", "Ocasional", "Con alta frecuencia", "Totalmente dependiente"]
            },
            {
                q: "Si mañana no está la persona que lo domina, ¿qué ocurre?",
                options: ["El proceso se detiene", "Se vuelve muy difícil", "Avanza con apoyo parcial", "Avanza con lentitud", "Nada cambia"]
            },
            {
                q: "¿Qué tan claras y repetibles son las reglas del proceso?",
                options: ["No hay reglas", "Reglas informales", "Medianamente definidas", "Documentadas", "Totalmente definidas y estables"]
            },
            {
                q: "¿Cuántas aplicaciones intervienen desde que inicia hasta que termina?",
                options: ["Una", "Dos", "Tres", "Cuatro", "Cinco o más"]
            },
            {
                q: "¿Qué volumen mensual maneja esta tarea?",
                options: ["< 50", "50–200", "200–500", "500–1,000", "> 1,000"]
            },
            {
                q: "¿Cuántas horas al mes consume hoy tu equipo en este trabajo?",
                options: ["< 20 h", "20–50", "50–100", "100–200", "> 200 h"]
            },
            {
                q: "¿Con qué frecuencia aparecen errores de digitación o formatos mal cargados?",
                options: ["< 5/mes", "5–15", "15–30", "30–60", "> 60/mes"]
            },
            {
                q: "¿Cuánto re-trabajo se genera porque los datos no cuadran solos?",
                options: ["< 5%", "5–10%", "10–20%", "20–35%", "> 35%"]
            },
            {
                q: "¿El atraso en este proceso afecta servicio, ingresos o cumplimiento?",
                options: ["No", "Bajo", "Medio", "Alto", "Impacto muy alto"]
            },
            {
                q: "¿Qué tan estandarizados están los datos de entrada?",
                options: ["Muy heterogéneos", "Heterogéneos", "Media", "Mayormente estables", "Totalmente estandarizados"]
            },
            {
                q: "Para organizaciones con ERP: ¿todo empieza y termina ahí?",
                options: ["No — los bordes quedan fuera", "Muy poco dentro", "Parcial", "Casi todo", "100% dentro del ERP"]
            },
            {
                q: "¿Cuántos pasos fuera del core nadie gobierna hoy?",
                options: ["Ninguno", "Muy pocos", "Media", "Muchos", "La mayoría del proceso"]
            }
        ];

        let currentIndex = 0;
        let totalScore = 0;

        // Referencias a elementos del DOM
        const introScreen = document.getElementById('intro-screen');
        const quizContainer = document.getElementById('quiz-container');
        const resultsScreen = document.getElementById('results-screen');
        const questionCard = document.getElementById('question-card');
        const questionTitle = document.getElementById('question-title');
        const optionsContainer = document.getElementById('options-container');
        const progressBar = document.getElementById('progress-bar');
        const progressText = document.getElementById('progress-text');
        const finalScoreEl = document.getElementById('final-score');
        const resultMessageEl = document.getElementById('result-message');

        function startAssessment() {
            // Animar salida del intro
            introScreen.classList.add('fade-exit-active');
            
            setTimeout(() => {
                introScreen.classList.add('hidden');
                quizContainer.classList.remove('hidden');
                renderQuestion();
            }, 400);
        }

        function renderQuestion() {
            const currentQ = questions[currentIndex];
            
            // Actualizar progreso
            const progressPercentage = ((currentIndex) / questions.length) * 100;
            progressBar.style.width = `${progressPercentage}%`;
            progressText.innerText = `${currentIndex + 1}/${questions.length}`;

            // Resetear animación de la tarjeta
            questionCard.classList.remove('fade-enter-active');
            void questionCard.offsetWidth; // Trigger reflow
            questionCard.classList.add('fade-enter-active');

            // Renderizar contenido
            questionTitle.innerText = `${currentIndex + 1}. ${currentQ.q}`;
            optionsContainer.innerHTML = '';

            currentQ.options.forEach((option, index) => {
                const points = index + 1; // 1 punto para la opción 1, 2 para la 2, etc.
                const btn = document.createElement('button');
                btn.className = 'w-full text-left p-5 rounded-xl bg-gray-800/50 border border-gray-700 option-btn text-lg font-medium text-gray-200 flex justify-between items-center group';
                btn.innerHTML = `
                    <span>${option}</span>
                    <i class="ph-bold ph-check-circle opacity-0 group-hover:opacity-100 text-kruger-cyan transition-opacity text-2xl"></i>
                `;
                btn.onclick = () => selectOption(points);
                optionsContainer.appendChild(btn);
            });
        }

        function selectOption(points) {
            totalScore += points;
            currentIndex++;

            if (currentIndex < questions.length) {
                // Animar salida de la pregunta actual
                questionCard.classList.remove('fade-enter-active');
                questionCard.classList.add('fade-exit-active');
                
                setTimeout(() => {
                    questionCard.classList.remove('fade-exit-active');
                    renderQuestion();
                }, 300);
            } else {
                showResults();
            }
        }

        function animateScore(targetScore) {
            let current = 0;
            const duration = 2000; // 2 segundos
            const increment = targetScore / (duration / 16); // 60fps aprox

            const timer = setInterval(() => {
                current += increment;
                if (current >= targetScore) {
                    finalScoreEl.innerText = targetScore;
                    clearInterval(timer);
                } else {
                    finalScoreEl.innerText = Math.floor(current);
                }
            }, 16);
        }

        function showResults() {
            quizContainer.classList.add('fade-exit-active');
            
            setTimeout(() => {
                quizContainer.classList.add('hidden');
                resultsScreen.classList.remove('hidden');
                resultsScreen.classList.add('fade-enter-active');
                
                // Animación del número
                animateScore(totalScore);

                // Mensaje dinámico basado en el score (Rango posible: 13 a 65)
                if (totalScore >= 50) {
                    resultMessageEl.innerHTML = "Tus procesos tienen una <strong>alta dependencia manual</strong>. Existe una oportunidad masiva para automatizar, reducir costos operativos y minimizar riesgos inmediatos.";
                } else if (totalScore >= 30) {
                    resultMessageEl.innerHTML = "Estás en un <strong>punto de inflexión</strong>. Hay cuellos de botella claros donde la automatización e integración de sistemas generará un ROI altísimo y rápido.";
                } else {
                    resultMessageEl.innerHTML = "Tienes procesos estructurados, pero la <strong>optimización con IA y automatización avanzada</strong> te llevará al siguiente nivel de escalabilidad y eficiencia.";
                }

            }, 400);
        }
    </script>
</body>
</html>
"""

# 3. Renderizar el componente en Streamlit
# Un height de 850px suele ser suficiente para esta vista, pero puedes ajustarlo.
# scrolling=False evita barras de desplazamiento dobles indeseadas.
components.html(codigo_html, height=850, scrolling=False)
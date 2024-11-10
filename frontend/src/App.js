import {useState } from 'react'




function App() {
  const [grades, setGrades] = useState([])
  function HandleGradesByParalell() {
    fetch('http://localhost:8000/api/v1/1/parallels/2/grades')
    .then(response => response.json())  
    .then(data => setGrades(data))
    .catch(error => console.error(error))
}
  return (
    <main>

    <body>
    <div class="container">
        <h1>Módulo de Calificaciones</h1>
        <ul>
            <li>
                <div class="button-container">
                    <span>Registrar calificación</span>
                    <button>Registrar</button>
                </div>
            </li>
            <li>
                <div class="button-container">
                    <span>Ver calificaciones por parallel_id</span>
                    <button onClick={HandleGradesByParalell}>Visualizar</button>
                    <showIf condition={grades.length > 0}>
                        <ul>                          
                            {grades.map(grade => (
                                <li key={grade._id}>
                                    <span>{grade.score}</span>
                                    <span>{grade.student_id}</span>
                                    <span>{grade.course_id}</span>
                                </li>
                            ))}
                        </ul>
                    </showIf>

                </div>
            </li>
            <li>
                <div class="button-container">
                    <span>Ver calificaciones por course_id</span>
                    <button>Visualizar</button>
                </div>
            </li>
            <li>
                <div class="button-container">
                    <span>Consultar calificación por grade_id</span>
                    <button>Consultar</button>
                </div>
            </li>
            <li>
                <div class="button-container">
                    <span>Eliminar calificación por grade_id</span>
                    <button>Eliminar</button>
                </div>
            </li>
            <li>
                <div class="button-container">
                    <span>Ver calificaciones de un estudiante por student_id</span>
                    <button>Visualizar</button>
                </div>
            </li>
            <li>
                <div class="button-container">
                    <span>Ver calificaciones por course_id</span>
                    <button>Visualizar</button>
                </div>
            </li>
            <li>
                <div class="button-container">
                    <span>Actualizar calificación por course_id</span>
                    <button>Actualizar</button>
                </div>
            </li>
        </ul>
    </div>
</body>



    </main>
  );
}

export default App;
import React, { useState} from 'react';
import { BotonBuscar } from './components/BotonBuscar.tsx';
import { Tarjeta } from './components/Tarjeta.tsx';
import { Input } from './components/Input.tsx';

function GradeCreator() {

    const [courseID, setCourseID] = useState(0);
    const [newScore, setNewScore] = useState(0);
    const [newStudentID, setNewStudentID] = useState(0)
    const [newParallel, setNewParallel] = useState(0)


    function CreateGrade() {
        const requestOptions = {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                "student_id": newStudentID,
                "score": newScore,
                "parallel_id": newParallel
            })
        };
        fetch(`http://localhost:8000/api/v1/${courseID}/grades`, requestOptions)
        .then((response) => {
            if(response.status === 200){
                window.location.href = '/'
            }
        })
        .catch(error => console.error(error));
    }

    return(
        <div>
            <div class="header">
                <h1>Módulo de calificaciones</h1>
            </div>
            <div className="container" style={{ padding: '10rem'}}>
                <Tarjeta style={{ width: '100%', height:'55%'}}>
                    <div style={{ padding: '1rem'}}>
                        <label htmlFor="search" style={{ display: 'block', marginBottom: '8px', marginTop: '16px' }}>ID de Curso</label>
                        <Input
                            type='number'
                            min={0}
                            max={100}
                            id="search"
                            placeholder="Ej: 65.5"
                            value={courseID}
                            onChange={(e) => setCourseID(Number(e.target.value))}
                        />
                        <label htmlFor="search" style={{ display: 'block', marginBottom: '8px', marginTop: '16px' }}>ID de paralelo</label>
                        <Input
                            type='number'
                            min={0}
                            max={100}
                            id="search"
                            placeholder="Ej: 65.5"
                            value={newParallel}
                            onChange={(e) => setNewParallel(Number(e.target.value))}
                        />
                        <label htmlFor="search" style={{ display: 'block', marginBottom: '8px', marginTop: '16px' }}>ID de estudiante</label>
                        <Input
                            type='number'
                            min={0}
                            max={100}
                            id="search"
                            placeholder="Ej: 65.5"
                            value={newStudentID}
                            onChange={(e) => setNewStudentID(Number(e.target.value))}
                        />
                        <label htmlFor="search" style={{ display: 'block', marginBottom: '8px', marginTop: '16px' }}>Calificación</label>
                        <Input
                            type='number'
                            min={0}
                            max={100}
                            id="search"
                            placeholder="Ej: 65.5"
                            value={newScore}
                            onChange={(e) => setNewScore(Number(e.target.value))}
                        />
                    </div>
                    <div style={{ display: 'flex', flexDirection: 'row'}}>
                        <BotonBuscar style={{backgroundColor: '#849324', color: 'black'}} onClick={() => CreateGrade()}>
                            Crear
                        </BotonBuscar>
                    </div>
                </Tarjeta>
            </div>
        </div>
    );
}

export default GradeCreator;
import React, { useState, useEffect} from 'react';
import { useParams } from 'react-router-dom';
import { BotonBuscar } from './components/BotonBuscar.tsx';
import { Tarjeta } from './components/Tarjeta.tsx';
import { Input } from './components/Input.tsx';

function GradeEditor() {

    const {gradeID} = useParams();
    const [gradeData, setGradeData] = useState([]);
    const [newGrade, setNewGrade] = useState(0);
    const [editorMode, setEditorMode] = useState("");

    useEffect(() => {
        fetch(`http://localhost:8000/api/v1/grades/${gradeID}`)
        .then((response) => response.json())
        .then((data) => setGradeData(data))
        .catch(error => console.error(error))
    },[gradeID, editorMode]);

    function UpdateGrade() {
        const requestOptions = {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' }
        };
        fetch(`http://localhost:8000/api/v1/${gradeData.course_id}/grades/${gradeID}?score=${newGrade}`, requestOptions)
        .then((response) => {
            if(response.status === 200){
                setEditorMode("");
                window.location.href = '/'
            }
        })
        .catch(error => console.error(error));
    }

    function DeleteGrade() {
        const requestOptions = {
            method: 'DELETE',
            headers: { 'Content-Type': 'application/json' }
        };
        fetch(`http://localhost:8000/api/v1/grades/${gradeID}`, requestOptions)
        .then((response) => {
            if(response.status === 200){
                setEditorMode("");
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
                {editorMode !== "edit" ?
                    <Tarjeta style={{ width: '100%', height:'25%'}}>
                        <div style={{ padding: '1rem'}}>
                            <p style={{ fontSize: '16px', fontWeight: 'bold' }}>ID de curso: {gradeData.course_id}</p>
                            <div style={{ paddingLeft: '0.5rem', paddingRight: '0.5rem' }}>
                                <p style={{ color: '#6b7280', fontSize: '14px', textAlign: 'left' }}>Paralelo: {gradeData.parallel_id}</p>
                                <p style={{ color: '#6b7280', fontSize: '14px', textAlign: 'left' }}>ID de estudiante: {gradeData.student_id}</p>
                                <p style={{ color: '#6b7280', fontSize: '14px', textAlign: 'left' }}>Calificación: {gradeData.score}</p>
                            </div>
                        </div>
                        <div style={{ display: 'flex', flexDirection: 'row'}}>
                            <BotonBuscar style={{backgroundColor: '#FFBC0A', color: 'black'}} onClick={() => setEditorMode("edit")}>
                                Modificar
                            </BotonBuscar>
                            <BotonBuscar style={{backgroundColor: '#BF0603'}} onClick={() => DeleteGrade()}>
                                Eliminar
                            </BotonBuscar>
                        </div>
                    </Tarjeta>
                :
                    <Tarjeta style={{ width: '100%', height:'25%'}}>
                    <div style={{ padding: '1rem'}}>
                        <label htmlFor="search" style={{ display: 'block', marginBottom: '8px', marginTop: '16px' }}>Nueva calificacion</label>
                            <Input
                                type='number'
                                min={0}
                                max={100}
                                id="search"
                                placeholder="Ej: 65.5"
                                value={newGrade}
                                onChange={(e) => setNewGrade(Number(e.target.value))}
                            />
                    </div>
                    <div style={{ display: 'flex', flexDirection: 'row'}}>
                        <BotonBuscar style={{backgroundColor: '#849324', color: 'black'}} onClick={() => UpdateGrade()}>
                            Modificar
                        </BotonBuscar>
                    </div>
                </Tarjeta>
                }
            </div>
        </div>
    );
}

export default GradeEditor;
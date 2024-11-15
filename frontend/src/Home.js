import React, { useState, useEffect} from 'react'
import { Boton } from './components/Boton.tsx'
import { Tarjeta } from './components/Tarjeta.tsx'
import { Input } from './components/Input.tsx'
import { BotonBuscar } from './components/BotonBuscar.tsx'
import { Link } from 'react-router-dom'

function Home() {

    const [grades, setGrades] = useState([])
    const [uri, setURI] = useState()

    //Parametros Filtro
    const [gradeRange, setGradeRange] = useState({ min: 0, max: 100 })
    const [filterMode, setFilterMode] = useState("course")
    const [gradesPerPage, setGradesPerPage] = useState(10)
    const [currentPage, setCurrentPage] = useState(1)

    //Parametros URI
    const [currentCourseID, setCurrentCourseID] = useState(1)
    const [currentParallelID, setCurrentParallelID] = useState(1)
    const [currentStudentID, setCurrentStudentID] = useState(1)

    const url = 'http://localhost:8000/api/v1/'

    useEffect(() => {
        setCurrentPage(1)
    }, [gradesPerPage])
    
    
    useEffect(() => {
        fetch(uri)
        .then((response) => response.json())
        .then((data) => setGrades(Array.from(data)))
        .catch(error => console.error(error))
    }, [uri]);

    function FilterParameters(props) {
        const currentFilter = props.currentFilter;

        let filterComponent;

        let requestURI;
        switch(currentFilter){
            case "course":
                filterComponent = (
                    <div style={{ marginBottom: '16px' }}>
                        <label htmlFor="search" style={{ display: 'block', marginBottom: '8px', marginTop: '16px' }}>ID de curso</label>
                        <Input
                            type='number'
                            min={0}
                            id="search"
                            placeholder="Ej: 1234"
                            value={currentCourseID}
                            onChange={(e) => setCurrentCourseID(Number(e.target.value))}
                        />
                        <div style={{ marginBottom: '16px' }}>
                            <label style={{ display: 'block', marginBottom: '8px', marginTop: '16px' }}>Rango de calificación</label>
                            <div style={{ display: 'flex', alignGrades: 'center' }}>
                                <span style={{ margin: '0 8px' }}>Entre</span>
                                <Input
                                    type="number"
                                    value={gradeRange.min}
                                    min={0}
                                    max={99}
                                    onChange={(e) => setGradeRange({ ...gradeRange, min: Number(e.target.value) })}
                                    style={{ width: '70px', marginRight: '8px' }}
                                />
                                <span style={{ margin: '0 8px' }}>y</span>
                                <Input
                                    type="number"
                                    value={gradeRange.max}
                                    min={1}
                                    max={100}
                                    onChange={(e) => setGradeRange({ ...gradeRange, max: Number(e.target.value) })}
                                    style={{ width: '70px' }}
                                />
                            </div>
                        </div>
                    </div>
                );
                requestURI = url + `${currentCourseID}/grades?page=${currentPage}&limit=${gradesPerPage}&min_score=${gradeRange.min}&max_score=${gradeRange.max}`;
                break;
            case "parallel":
                filterComponent =(
                    <div style={{ marginBottom: '16px' }}>
                        <label htmlFor="search" style={{ display: 'block', marginBottom: '8px', marginTop: '16px' }}>ID de curso</label>
                        <Input
                            type='number'
                            min={0}
                            id="search"
                            placeholder="Ej: 1234"
                            value={currentCourseID}
                            onChange={(e) => setCurrentCourseID(Number(e.target.value))}
                        />
                        <label htmlFor="search" style={{ display: 'block', marginBottom: '8px', marginTop: '16px'  }}>ID de paralelo</label>
                        <Input
                            type='number'
                            id="search"
                            min={0}
                            placeholder="Ej: 1234"
                            value={currentParallelID}
                            onChange={(e) => setCurrentParallelID(Number(e.target.value))}
                        />
                    </div>
                );
                requestURI = url + `${currentCourseID}/parallels/${currentParallelID}/grades?page=${currentPage}&limit=${gradesPerPage}`;
                break;
            case "student":
                filterComponent =(
                    <div style={{ marginBottom: '16px' }}>
                        <label htmlFor="search" style={{ display: 'block', marginBottom: '8px', marginTop: '16px' }}>ID de estudiante</label>
                        <Input
                            type='number'
                            min={0}
                            id="search"
                            placeholder="Ej: 1234"
                            value={currentStudentID}
                            onChange={(e) => setCurrentStudentID(Number(e.target.value))}
                        />
                        <div style={{ marginBottom: '16px' }}>
                            <label style={{ display: 'block', marginBottom: '8px', marginTop: '16px'  }}>Rango de calificación</label>
                            <div style={{ display: 'flex', alignGrades: 'center' }}>
                                <span style={{ margin: '0 8px' }}>Entre</span>
                                <Input
                                    type="number"
                                    value={gradeRange.min}
                                    min={0}
                                    max={99}
                                    onChange={(e) => setGradeRange({ ...gradeRange, min: Number(e.target.value) })}
                                    style={{ width: '70px', marginRight: '8px' }}
                                />
                                <span style={{ margin: '0 8px' }}>y</span>
                                <Input
                                    type="number"
                                    value={gradeRange.max}
                                    min={1}
                                    max={100}
                                    onChange={(e) => setGradeRange({ ...gradeRange, max: Number(e.target.value) })}
                                    style={{ width: '70px' }}
                                />
                            </div>
                        </div>
                    </div>
                );
                requestURI = url + `students/${currentStudentID}/grades?page=${currentPage}&limit=${gradesPerPage}&min_score=${gradeRange.min}&max_score=${gradeRange.max}`;
                break;
            default:
                filterComponent =(
                    <div style={{ marginBottom: '16px' }}>
                        <p>Modo incorrecto</p>
                    </div>
                );
        }
        return [
            filterComponent,
            <div>
                <label htmlFor="grades-per-page" style={{ display: 'block', marginBottom: '8px' }}>Calificaciones por página</label>
                <select
                    id="grades-per-page"
                    value={gradesPerPage}
                    onChange={(e) => setGradesPerPage(Number(e.target.value))}
                    style={{
                    width: '100%',
                    padding: '8px',
                    border: '1px solid #d1d5db',
                    borderRadius: '4px',
                    fontSize: '14px',
                    }}
                >
                    <option value={5}>5</option>
                    <option value={10}>10</option>
                    <option value={20}>20</option>
                    <option value={50}>50</option>
                </select>
            </div>,
            <BotonBuscar style={{backgroundColor: '#0075F2'}} onClick={() => setURI(requestURI)}>
                Buscar
            </BotonBuscar>
        ]
    }
    return (
    <main>
        <div className="header">
            <h1>Módulo de calificaciones</h1>
        </div>
        <div className="container">
            <div className="sidebar">
                <div>
                    <label htmlFor="filter-type" style={{ display: 'block', marginBottom: '8px' }}>Filtro</label>
                    <select
                        id="filter-type"
                        value={filterMode}
                        onChange={(e) => setFilterMode(e.target.value)}
                        style={{
                        width: '100%',
                        padding: '8px',
                        border: '1px solid #d1d5db',
                        borderRadius: '4px',
                        fontSize: '14px',
                        }}
                    >
                        <option value={"course"}>Por curso</option>
                        <option value={"parallel"}>Por paralelo</option>
                        <option value={"student"}>Por estudiante</option>
                    </select>
                </div>
                <FilterParameters currentFilter={filterMode}/>
            </div>
            <div className="mainContent">
                <h1 style={{ fontSize: '24px', fontWeight: 'bold', marginBottom: '16px' }}>Calificaciones</h1>
                    <div style={{ display: 'grid', gap: '16px', gridTemplateColumns: 'repeat(auto-fill, minmax(200px, 1fr))' }}>
                        {grades.map((grade) => (
                            <Tarjeta key={grade._id}>
                                <Link to={`grade/${grade.grade_id}`}>
                                    <button className='cardButton'>
                                        <p style={{ fontSize: '16px', fontWeight: 'bold' }}>ID de curso: {grade.course_id}</p>
                                        <div style={{ paddingLeft: '0.5rem', paddingRight: '0.5rem' }}>
                                            <p style={{ color: '#6b7280', fontSize: '14px', textAlign: 'left' }}>Paralelo: {grade.parallel_id}</p>
                                            <p style={{ color: '#6b7280', fontSize: '14px', textAlign: 'left' }}>ID de estudiante: {grade.student_id}</p>
                                            <p style={{ color: '#6b7280', fontSize: '14px', textAlign: 'left' }}>Calificación: {grade.score}</p>
                                        </div>
                                    </button>
                                </Link>
                            </Tarjeta>
                        ))}
                    </div>
                <div style={{ marginTop: '24px', display: 'flex', justifyContent: 'space-between', alignGrades: 'center' }}>
                    <p style={{ fontSize: '14px', color: '#6b7280' }}>
                        Mostrando {grades.length} calificaciones
                    </p>
                    <div style={{ display: 'flex', alignGrades: 'center' }}>
                        <Boton
                            onClick={() => setCurrentPage((prev) => Math.max(prev - 1, 1))}
                            style={{ marginRight: '8px' }}
                        >
                            Anterior
                        </Boton>
                        <span style={{ margin: '0 16px' }}>Página {currentPage}</span>
                        <Boton
                            onClick={() => setCurrentPage((prev) => prev + 1)}
                        >
                            Siguiente
                        </Boton>
                    </div>
                </div>
            </div>
        </div>
    </main>
  );
}

export default Home;
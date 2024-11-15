import React from 'react'

interface CardProps {
  children: React.ReactNode
  style?: React.CSSProperties
}

export const Tarjeta: React.FC<CardProps> = ({ children, style }) => {
  const cardStyle: React.CSSProperties = {
    border: '1px solid #e5e7eb',
    display: 'flex',
    flexDirection: 'column',
    borderRadius: '8px',
    padding: '0',
    backgroundColor: 'white',
    boxShadow: '0 1px 3px 0 rgba(0, 0, 0, 0.1)',
    ...style,
  }

  return <div style={cardStyle}>{children}</div>
}
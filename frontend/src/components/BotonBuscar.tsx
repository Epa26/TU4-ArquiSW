import React from 'react'

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {}

export const BotonBuscar: React.FC<ButtonProps> = ({ children, style, ...props }) => {
  const inputStyle: React.CSSProperties = {
    marginTop: '1rem',
    padding: '8px 16px',
    borderRadius: '4px',
    border: 'none',
    fontSize: '14px',
    width: '100%',
    color: '#ffffff',
    ...style,
  }

  return(
    <button style={inputStyle} {...props}>
        {children}
    </button>
    )
}
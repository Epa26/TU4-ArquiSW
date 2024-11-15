import React from 'react'

interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {}

export const Input: React.FC<InputProps> = ({ style, ...props }) => {
  const inputStyle: React.CSSProperties = {
    width: 'auto',
    margin: '0.2rem',
    padding: '0.2rem',
    fontSize: '1rem',
    lineHeight: '1.5',
    border: '1px solid #d1d5db',
    borderRadius: '4px',
    ...style,
  }

  return <input style={inputStyle} {...props} />
}
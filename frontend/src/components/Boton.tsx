import React from 'react'

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'default' | 'outline' | 'ghost'
}

export const Boton: React.FC<ButtonProps> = ({ children, variant = 'default', style, ...props }) => {
  const baseStyle: React.CSSProperties = {
    padding: '8px 16px',
    borderRadius: '4px',
    cursor: 'pointer',
    fontSize: '14px',
    transition: 'background-color 0.2s',
  }

  const variantStyles: Record<string, React.CSSProperties> = {
    default: {
      backgroundColor: '#3b82f6',
      color: 'white',
      border: 'none',
    },
    outline: {
      backgroundColor: 'transparent',
      color: '#3b82f6',
      border: '1px solid #3b82f6',
    },
    ghost: {
      backgroundColor: 'transparent',
      color: '#3b82f6',
      border: 'none',
    },
  }

  const combinedStyle = { ...baseStyle, ...variantStyles[variant], ...style }

  return (
    <button style={combinedStyle} {...props}>
      {children}
    </button>
  )
}
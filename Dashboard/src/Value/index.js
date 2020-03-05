import React from 'react'

function Value(props) {
  return (
    <div>
      <p style={{fontWeight: "bold"}}>{props.name}</p>
      <p>
        {props.value}
      </p>
    </div>
  )
}

export default Value
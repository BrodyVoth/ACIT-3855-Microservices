import React, {useState, useEffect} from 'react'
import Value from "./Value";
import axios from 'axios'

document.title = 'Sleep Stats'


function App() {
  const [value, setValue] = useState('value1')
  const [value2, setValue2] = useState('value2')
  const [value3, setValue3] = useState('value3')
  const [value4, setValue4] = useState('value4')
  const [value5, setValue5] = useState('value5')



  const getValue = () => {
    axios.get('http://127.0.0.1:8100/report/stats')
      .then(json => {
        console.log(json.data)
        setValue(json.data.num_sleep_stats)
        setValue2(json.data.num_day_stats)
      })
    axios.get('http://127.0.0.1:8120/log/sleep_stats?offset=3')
    .then(json => {
      console.log(json.data)
      setValue3(json.data.payload.feeling + ': ' + json.data.payload.notes)
      // document.title = json.data.value
    })
    axios.get('http://127.0.0.1:8120/log/day_stats')
    .then(json => {
      console.log(json.data)
      setValue4(json.data.payload.mood + ': ' + json.data.payload.notes)
      // document.title = json.data.value
    })
    setValue5(Date())
  }


  useEffect(() => {
    getValue();
    setInterval(getValue, 2000)
  }, [value])

  return (
    <div style={{border: "2px solid black", textAlign: "center", width: 500, margin: "auto"}}>
      <img alt="Sleep Logo" height="100" width="100" src={require('./sleeplogo.png')}></img>
      <Value value={value} name={"Sleep Stats Count"} />
      <Value value={value2} name={"Day Stats Count"} />
      <Value value={value3} name={"3rd Sleep Stat"} />
      <Value value={value4} name={"First Day Stat"} />
      <Value value={value5} name={"Last Updated"} />
    </div>
  )
}

export default App
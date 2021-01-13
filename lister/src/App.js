import './App.css';
import 'wingcss/dist/wing.css';
import Form from './form/index';
import { useState } from 'react';
import Table from './table';

function App() {
  const [result, setResult] = useState();
  if(result) {
    const sorted = result.sort((a, b) => {
      return a.chunks.length <= b.chunks.length ? 1 : -1;
    });
    return (
      <>
        <button className="outline" onClick={() => setResult(undefined)}>Start over</button>
        <Table result={sorted} />
      </>
    );
  }
  return (
    <div className="App">
      <Form onResult={setResult} />
    </div>
  );
}

export default App;

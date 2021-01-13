import React from 'react'

function Table({ result }) {
  return (
    <table style={{ width: '100%' }} border="1">
      <thead>
        <tr>
          <td>Item</td>
          <td>Occurrences</td>
          <td>Who mentioned</td>
          <td>Who liked</td>
        </tr>
      </thead>
      <tbody>
        {result.map((r) => {
          return (
            <tr>
              <td>{r.name}</td>
              <td>{r.chunks.length}</td>
              <td>{r.chunks.map(c => `@${c.by} `)}</td>
            </tr>
          );
        })}
      </tbody>
    </table>
  )
}

export default Table

function TableBody({ tableData, columns }) {

    // Functions go here

    return (
     <tbody>
      {tableData.map(([name, value]) => {
        value['name'] = name
       return (
        <tr key={name}>
         {columns.map(({ key }) => {
          const tData = value[key] ? value[key] : "N/A";
          return <td key={key}>{tData}</td>;
         })}
        </tr>
       );
      })}
     </tbody>
    );
   };
   
   export default TableBody;
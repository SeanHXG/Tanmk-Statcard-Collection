function TableHead({columns}) {

    // Functions go here

    return (
        <thead>
            <tr>
            {columns.map(({ category, key }) => {
                return <th key={key}>{category}</th>;
            })}
            </tr>
        </thead>
    );
};
   
export default TableHead;
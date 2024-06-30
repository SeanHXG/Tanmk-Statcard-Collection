import PartTable from '../../components/PartTable/PartTable.js'

function ComparePage({data}){
    let filters = {type: 'guns'}
    console.log()
    return (
        <div className="table_container">
            <PartTable filters={filters} data={data}/>
        </div>
    );
};

export default ComparePage
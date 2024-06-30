import React, { useEffect, useState } from 'react'
import 'bootstrap/dist/css/bootstrap.css'
import './PartCard.css'
import Card from 'react-bootstrap/Card'
import {  } from 'react-bootstrap-icons'
import { useNavigate } from 'react-router'

function PartCard({type, name, info}) {

    let img = '/images/default.png'
    try{
        img = '/images/' + type + '/' + name.trim() + '.png'
    }
    catch{
        console.error('Image failed to load: ' + name + '[' + type + ']')
    }

    function Turretless(){
        console.log(info)
        if (info.turretless === 'Yes'){
            return <h5 className="badge tag">Turretless</h5>
        }
        return null
    }
    function Wheeled(){
        
        if(info.wheeled === 'Yes'){
            return <h5 className="badge tag">Wheeled</h5>
        }
        return null
    }
    /*const navigate = useNavigate();
    const handleCardClick = () => {
        navigate(`/recipes/${info.id}/details`, { state: { scrollToTop: true } });
      };
    */

    return(
        <Card className='statcard-wrapper' /*onClick={handleCardClick}*/>
            <div className="statcard-img-tag-wrapper">
                <Card.Img className="statcard-img" variant="top" src={img} alt={name} />
                <div className="tags-wrapper">
                    <Turretless/> <Wheeled/>
                </div>
            </div>
            <Card.Body>
                <h4 className="card-title text-no-overflow"><b>{name}</b></h4>
                <i className="text-no-overflow">{info.obtain}</i>
            </Card.Body>
        </Card>
    );
}

export default PartCard;
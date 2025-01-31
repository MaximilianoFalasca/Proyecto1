"use client"
import React from 'react';
import CustomIcon from '../../../components/CustomIcon';
import axios from 'axios';
import { useSearchParams } from "next/navigation";
import { API_URL } from '@/utils/config';
import { Box, Button } from '@mui/material';
import IconButton from '@mui/material/IconButton';
import Divider from '@mui/material/Divider';
import { blue } from '@mui/material/colors';

interface Asiento{
  numero: number;
  matricula: string;
  precio: number;
  estado: string;
}

export default function PruebaPage() {
  const searchParams = useSearchParams();
  const numero = searchParams.get("numero");
  const fechaSalida = searchParams.get("fechaSalida");
  const [asientos,setAsientos] = React.useState<any | any>(null)
  const [seleccionados,setSeleccionados] = React.useState<Asiento[]>([])
  const [vuelo,setVuelo] = React.useState<any | any>(null)

  React.useEffect(() => {
    async function getAsientos(){
      try{
        let fecha = fechaSalida?.split(" ")
        let fechaProcesada = fecha?.join("T")

        let response = await axios.get(`${API_URL}/vuelos/${numero}/${fechaProcesada}/asientos`)
        
        setAsientos(response.data)

        response = await axios.get(`${API_URL}/vuelos/${numero}/${fechaProcesada}`)

        setVuelo(response.data)
      } catch (error) {
        console.error(error);
      }
    }

    getAsientos()
  },[numero, fechaSalida])

  function normalizarFecha(fecha:string){
    let fechaNormalizada = new Date(fecha).toLocaleString();

    return fechaNormalizada;
  }

  function seleccionAsiento(asiento:Asiento){
    setAsientos(asientos.map((asientoMap:Asiento) => {
      if (asientoMap.numero == asiento.numero) {
        if (asientoMap.estado=="libre") {
          asientoMap.estado="seleccionado"
          setSeleccionados([...seleccionados, asientoMap])
        } else if (asientoMap.estado=="seleccionado") {
          asientoMap.estado="libre"
          setSeleccionados([...seleccionados.filter((asientoSeleccionado:Asiento) => asientoSeleccionado.numero != asientoMap.numero)])
        }
      }
      return asientoMap
    }))
  }

  function obtenerObjetosAsientos(){
    console.log("asientos:",asientos)
    if (!asientos || asientos.length < 4) return <p>Cargando asientos o no hay suficientes disponibles.</p>;

    if (asientos.length < 4) return <p>No hay suficientes asientos disponibles.</p>;

    const rowsCol1 = []
    const rowsCol2 = []

    let key = 0

    for (let index = 3; index < asientos.length; index+=4) {
      rowsCol1.push(
        <div key={key++} style={{ display: 'flex', flexDirection: 'row'}} >
          <IconButton 
            key={index-3} 
            disabled={asientos[index-3].estado=="inhabilitado" || asientos[index-3].estado=="ocupado"} 
            disableRipple={true} 
            data-numero={asientos[index-3].numero} 
            data-matricula={asientos[index-3].matricula} 
            data-precio={asientos[index-3].precio} 
            onClick={(e) => seleccionAsiento(asientos[index-3])}
          >
            <CustomIcon 
              color={asientos[index-3].estado=="libre"?"disabled":asientos[index-3].estado=="inhabilitado" || asientos[index-3].estado=="ocupado"?"error":"primary"}
              fontSize='large'
            />
          </IconButton>
          <IconButton 
            key={index-2} 
            disabled={asientos[index-2].estado=="inhabilitado" || asientos[index-2].estado=="ocupado"} 
            disableRipple={true} 
            data-numero={asientos[index-2].numero} 
            data-matricula={asientos[index-2].matricula} 
            data-precio={asientos[index-2].precio} 
            onClick={(e) => seleccionAsiento(asientos[index-2])}
          >
            <CustomIcon 
              color={asientos[index-2].estado=="libre"?"disabled":asientos[index-2].estado=="inhabilitado" || asientos[index-2].estado=="ocupado"?"error":"primary"}
              fontSize='large'
            />
          </IconButton>
        </div>
      )
      rowsCol2.push(
        <div key={key++} style={{ display: 'flex', flexDirection: 'row'}} >
          <IconButton 
            key={index-1} 
            disabled={asientos[index-1].estado=="inhabilitado" || asientos[index-1].estado=="ocupado"} 
            disableRipple={true} 
            data-numero={asientos[index-1].numero} 
            data-matricula={asientos[index-1].matricula} 
            data-precio={asientos[index-1].precio} 
            onClick={(e) => seleccionAsiento(asientos[index-1])}
          >
            <CustomIcon 
              color={asientos[index-1].estado=="libre"?"disabled":asientos[index-1].estado=="inhabilitado" || asientos[index-1].estado=="ocupado"?"error":"primary"}
              fontSize='large'
            />
          </IconButton>
          <IconButton 
            id={`${index}`}
            key={index} 
            disabled={asientos[index].estado=="inhabilitado" || asientos[index].estado=="ocupado"} 
            disableRipple={true} data-numero={asientos[index].numero} 
            data-matricula={asientos[index].matricula} 
            data-precio={asientos[index].precio} 
            onClick={(e) => {
              console.log(e.currentTarget) 
              seleccionAsiento(asientos[index])
            }}
            component="button"
          >
            <CustomIcon 
              color={asientos[index].estado=="libre"?"disabled":asientos[index].estado=="inhabilitado" || asientos[index].estado=="ocupado"?"error":"primary"}
              fontSize='large'
            />
          </IconButton>
        </div>
      )
    }

  return (
    <Box style={{ display: 'flex', justifyContent: 'space-around', alignItems:'center', flex: 1 }}>
      <div style={{ display: 'flex', flexDirection: 'column'}}>
        {rowsCol1}
      </div>
      <div style={{ display: 'flex', flexDirection: 'column'}}>
        {rowsCol2}
      </div>
    </Box>
    )
  }

  function mostrarVuelo(){
    if (vuelo) {
      return (
        <Box style={{ display: 'flex', flexDirection: 'column', justifyContent: 'center', alignItems: 'center', flex: 1 }}>
          <Box style={{ display: 'flex', flexDirection: 'column', justifyContent: 'center', alignItems: 'center', flex: 1, border: '1px solid', borderColor: blue[200], width: '100%' }}>
            <h1>Tu Pedido</h1>
            <div style={{ display: 'flex', flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', width: '100%', paddingLeft: '30px', paddingRight: '30px'}}>
              <p>Numero Vuelo</p>
              <p>{vuelo.nro}</p>
            </div>
            <div style={{ display: 'flex', flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', width: '100%', paddingLeft: '30px', paddingRight: '30px'}}>
              <p>Origen</p>
              <p>{vuelo.aeropuertoSalida.nombre}, {vuelo.aeropuertoSalida.ciudad}, {vuelo.aeropuertoSalida.pais}</p>
            </div>
            <div style={{ display: 'flex', flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', width: '100%', paddingLeft: '30px', paddingRight: '30px'}}>
              <p>Destino</p>
              <p>{vuelo.aeropuertoLlegada.nombre}, {vuelo.aeropuertoLlegada.ciudad}, {vuelo.aeropuertoLlegada.pais}</p>
            </div>
            <div style={{ display: 'flex', flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', width: '100%', paddingLeft: '30px', paddingRight: '30px'}}>
              <p>Fecha y hora de salida</p>
              <p>{normalizarFecha(vuelo.fechaYHoraSalida)}</p>
            </div>
            <div style={{ display: 'flex', flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', width: '100%', paddingLeft: '30px', paddingRight: '30px'}}>
              <p>Fecha y hora de llegada</p>
              <p>{normalizarFecha(vuelo.fechaYHoraLlegada)}</p>
            </div>
            <Divider orientation="horizontal" variant="middle" flexItem />
            <div style={{ display: 'flex', flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', width: '100%', paddingLeft: '30px', paddingRight: '30px'}}>
              <p>Ubicaciones</p>
              <p>{seleccionados.map((asiento:Asiento) => asiento.numero).join(", ")}</p>
            </div>
            <Divider orientation="horizontal" variant="middle" flexItem />
            <div style={{ display: 'flex', flexDirection: 'row', justifyContent: 'center', alignItems: 'center', width: '95%', backgroundColor: blue[300], margin: '10px'}}>  
              <p>TOTAL:</p>
              <p style={{ marginLeft: 10 }}>${seleccionados.reduce((acc:number, asiento:Asiento) => acc + asiento.precio,0)}</p>
            </div>
          </Box>
          <Box style={{ display: 'flex', flexDirection: 'row', justifyContent: 'center', alignItems: 'center', width:'100%', marginTop: '10px', gap: '10px' }}>
            <Button variant="outlined" onClick={() => console.log("comprar")}>
              Comprar
            </Button>
            <Button variant="outlined" onClick={() => console.log("cancelar")}>
              Cancelar
            </Button>
          </Box>
        </Box>
      )
    }
  }

  return (    
    <Box style={{ display: 'flex', justifyContent: 'space-around', alignItems:'center', height: '100vh', width:'100%', flex: 1}}>
      {obtenerObjetosAsientos()}
      {mostrarVuelo()}
    </Box>
  );
}
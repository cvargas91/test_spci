import { api } from "boot/axios";

export function reqActores(context) {
    api
        .get("api/actor/getActores/")
        .then((response) => {   
            context.commit("setActores", response.data.datos);
            //context.commit("setTotalActores",)
        })
        .catch(() => {
            console.log("error req actores");
        });
}

export function reqDetalleActor(context, actores) {
    api
        .get("api/actor/getActoresPanel/"+actores)
        .then((response) => {            
            context.commit("setActor", response.data.results);
            //context.commit("setTotalActores",)
        })
        .catch(() => {
            console.log("error req actores");
        });
}

export function reqDirecciones(context) {
    api
        .get("api/actor/getDirecciones/")
        .then((response) => {            
            context.commit("setDireccion", response.data.datos);
        })
        .catch(() => {
            console.log("error req direccion");
        });
}

export function reqUnidades (context) {
    api
        .get("api/actor/getUnidades/")
        .then((response) => {            
            context.commit("setUnidad", response.data.datos);
        })
        .catch(() => {
            console.log("error req unidad");
        });
}

export function reqUnidad(context, direccion) {
    api
    .get("api/actor/getDireccion/?dependencia="+ direccion)
    .then((response) => {            
        context.commit("setUnidad", response.data.datos);
    })
    .catch(() => {
        console.log("error req unidad");
    });
}

export function reqFiltroActores(context, unidad) {
    api
    .get("api/actor/getDireccion/?dependencia="+ unidad)
        .then((response) => {   
            context.commit("setActores", response.data.datos);
        })
        .catch(() => {
            console.log("error req actores");
        });
}

export function limpiaUnidad(context) {
    context.commit("setUnidad", null);
}

export function limpiaActores(context) {
    context.commit("setActores" , null);
}
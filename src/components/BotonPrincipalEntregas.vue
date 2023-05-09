<template>
  {{ validaEtiqueta () }}
  <div 
        class="text-h6 q-mb-md"
        v-if="adjuntos">
        Acción <b> Sin archivos adjuntos</b>.
  </div>
  <q-btn
    v-if="seRenderea"
    :label="etiqueta"
    color="light-blue-10"
    @click="accionBoton"
  />
</template>
<script>
import {ref, defineComponent } from "vue";
import { useStore } from "vuex";
import { useRouter } from "vue-router";

export default defineComponent({
  props: {
    usuario: Object,
    entrega: Object,
    tipoEntrega: String,
  },
  emits:["ajuntosEntregas","mantencion"],
  setup(props, {emit}) {        
    const store = useStore();
    const router = useRouter();
    const seRenderea = ref(true);
    const etiqueta = ref("");
    const accion = ref("");
    const adjuntos = ref(false);

    //VARIABLE "mantencionPOA2023" implica control a actualizaciones relacionadas al nuevo modelo y sábana de datos
    const mantencionPOA2023 = ref(false);

    const validaEtiqueta = () => {
      if(!mantencionPOA2023.value){
        if (props.entrega.estado == "Finalizado") 
            seRenderea.value = false;
        else if (props.entrega.estado == "Enviado a UPCI" && props.usuario.perfil.esAnalistaUPCI) {
            etiqueta.value = "   Finalizar  ";
            accion.value = "UPCIFinaliza";
        } else if (props.entrega.estado == "Enviado al líder" && props.usuario.perfil.esEncargado) {
            etiqueta.value = " Enviar a UPCI ";
            accion.value = "liderEnvia";
        } else if (props.entrega.estado == "Borrador" && props.usuario.id == props.entrega.usuario.id) {
            etiqueta.value = " Enviar al líder ";
            accion.value = "colabEnvia";
        } else if(props.entrega.estado == "Rechazado por líder" && props.usuario.id == props.entrega.usuario.id){
            etiqueta.value = " Enviar al líder ";
            accion.value = "colabEnvia";
        } else if (props.entrega.estado == "Rechazado por UPCI" && props.usuario.id == props.entrega.usuario.id) { 
            etiqueta.value = " Enviar a UPCI ";
            accion.value = "liderEnvia";
        } else {
            seRenderea.value = false;
        }
      }
    };
    
        

    return {      
      etiqueta,
      seRenderea,
      adjuntos,
      validaEtiqueta,
      accionBoton: () => {
        switch (accion.value) {
          case "colabEnvia":
            if (!props.entrega.adjuntos || !props.entrega.adjuntos.length){            
                adjuntos.value = true;
                seRenderea.value = false;
                emit("ajuntosEntregas", adjuntos.value);                
            }else{
              adjuntos.value = false;              
              store.dispatch("entrega/workflowEnviaAlLider", {
                entrega_id: props.entrega.id,
                entrega_tipo: props.tipoEntrega,
              });
            }                                    
            break;
          case "liderEnvia":
            store.dispatch("entrega/workflowLiderDaVistoBueno", {
              entrega_id: props.entrega.id,
              entrega_tipo: props.tipoEntrega,
            });
            break;
          case "UPCIFinaliza":
            store.dispatch("entrega/workflowUPCIDaVistoBueno", {
              entrega_id: props.entrega.id,
              entrega_tipo: props.tipoEntrega,
              //comentario_upci: txtCumplimiento.value,
            });
            break;
        }
      },
    };
  },
});
</script>

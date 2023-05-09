<template>
  {{ validaEtiqueta () }}
  <DescartaEntrega
    :entrega="entrega"
    :mostrar="mostrarPopupDescartar"
    :tipoEntrega="tipoEntrega"
    @update:mostrar="mostrarPopupDescartar = $event"
  />
  <q-btn
    v-if="seRenderea"
    :label="etiqueta"
    color="negative"
    @click="accionBoton"
  />
</template>
<script>
import { ref, defineComponent } from "vue";
import { useStore } from "vuex";
import { useRouter } from "vue-router";
import DescartaEntrega from "src/components/DescartaEntrega.vue";

export default defineComponent({
  components: {
    DescartaEntrega,
  },
  props: {
    usuario: Object,
    entrega: Object,
    tipoEntrega: String,
  },
  emits:['mantencion'],
  setup(props, {emit}) {
    const router = useRouter();
    const store = useStore();
    const seRenderea = ref(true);
    const etiqueta = ref("");
    const accion = ref("");
    const mostrarPopupDescartar = ref(false);
    //VARIABLE "mantencionPOA2023" implica control a actualizaciones relacionadas al nuevo modelo y sábana de datos
    const mantencionPOA2023 = ref(false);

    const validaEtiqueta = () => {
      if(!mantencionPOA2023.value){
        if (props.entrega.estado == "Finalizado") 
            seRenderea.value = false;
        else if (
          props.entrega.estado == "Enviado a UPCI" &&
          props.usuario.perfil.esAnalistaUPCI
        ) {
            etiqueta.value = "Rechazar";
            accion.value = "UPCIRechaza";
        } else if (
          props.entrega.estado == "Enviado al líder" &&
          props.usuario.perfil.esEncargado
        ) {
            etiqueta.value = "Rechazar";
            accion.value = "liderRechaza";
        } else if (
          props.entrega.estado == "Borrador" &&
          props.usuario.id == props.entrega.usuario.id
        ) {
            etiqueta.value = "Descartar";
            accion.value = "colabDescarta";
        } else seRenderea.value = false;
      }
                
    };
    
    return {
      etiqueta,
      seRenderea,
      mostrarPopupDescartar,
      entrega: props.entrega,
      tipoEntrega: props.tipoEntrega,
      validaEtiqueta,
      accionBoton: () => {
        if (accion.value == "colabDescarta") mostrarPopupDescartar.value = true;
        else if (accion.value == "liderRechaza") {
          store.dispatch("entrega/setEntregaARechazar", {
            entrega: props.entrega,
            tipoEntrega: props.tipoEntrega,
            mandante: "lider",
          });
          router.push("rechazaEntrega");
        } else if (accion.value == "UPCIRechaza") {
          store.dispatch("entrega/setEntregaARechazar", {
            entrega: props.entrega,
            tipoEntrega: props.tipoEntrega,
            mandante: "UPCI",
          });
          router.push("rechazaEntrega");
        }
      },
    };
  },
});
</script>

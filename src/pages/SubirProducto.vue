<template>
  <div class="q-pa-md">
    <PopupCancelarNuevaEntrega
      :mostrar="mostrarPopupCancelar"
      @update:mostrar="mostrarPopupCancelar = $event"
      @respuestaPopup="handlerPopupCancelar"
    />
    <div v-if="entrega.estadoWorkflow == 'EnviadoAlLider'">
      <div class="text-h6">¡Felicitaciones!</div>
      <p>Se ha enviado el nuevo borrador al líder del equipo</p>
      <q-btn
        label="OK. Ir a la bandeja de entregas"
        class="q-ma-sm"
        to="bandejaEntregas"
        color="primary"
      />
    </div>
    <div v-else-if="producto.nuevoProducto">
      <div class="text-h6">
        ¿Está listo tu nuevo producto para ser revisado por el líder del equipo?
      </div>
      <div>
        <q-btn
          label="No no no, déjalo como borrador. Lo enviaré más tarde"
          class="q-ma-sm"
          to="bandejaEntregas"
          color="primary"
        />
        <q-btn
          class="q-ma-sm"
          label="Sí, envíalo al líder"
          @click="enviaAlLider"
          color="secondary"
        />
      </div>
    </div>
    <div v-else-if="entrega.nuevaEntrega">
      <q-stepper
        v-model="step"
        ref="stepper"
        animated
        header-class="tablaAcciones"
      >
        <q-step
          :name="1"
          title="MDV"
          icon="settings"
          :done="step > 1"
          class="tarjetaAmarilla"
        > 
          <div class="text-h6">
            Seleccione los Hitos y el Medio de Verificación (MDV) de
            {{ entrega.nuevaEntrega.id_uaysen }} que cumplen con esta entrega
          </div>
          <div v-if="accion.hitos.length">
            <q-select
              label="Hitos"
              use-chips
              stack-label
              :multiple="defineSeleccion(entrega.nuevaEntrega.anio)"
              v-model="hitosSeleccionados"
              :options="accion.hitos"
              option-value="id"
              option-label="nombre"
            />
          </div>
          <div v-else>
            <q-banner class="bg-primary text-white">
              No hay hitos asociados a la acción #{{
                entrega.nuevaEntrega.id_accion
              }}. Contacta a UPCI para revisar el caso
            </q-banner>
          </div>
          <div v-if="accion.MDVs.length">
            <q-select
              label="Medio de Verificación"
              v-model="mdvSeleccionado"
              :options="accion.MDVs"
              option-label="nombre"
            />
          </div>
          <div v-else>
            <q-banner class="bg-primary text-white">
              No hay Medios de Verificación asociados a la acción
              {{ entrega.nuevaEntrega.id_accion }}. Contacta a UPCI con los
              antecedentes necesarios para revisar el caso
            </q-banner>
          </div>
        </q-step>
        <q-step
          :name="2"
          title="Describe la entrega"
          caption="Optional"
          icon="create_new_folder"
          :done="step > 2"
          class="tarjetaAmarilla"
        >
          <div class="text-h6">Describe la actual entrega</div>
          <q-input
            v-model="descripcionMDV"
            filled
            type="textarea"
            placeholder="Explica los avances más importantes que se cumplen con esta entrega. Esto permitirá acelerar el proceso de revisión por parte del equipo UPCI"
          />
        </q-step>

        <q-step
          :name="3"
          title="Adjunta"
          icon="assignment"
          class="tarjetaAmarilla"
        >
          {{ defineDescripcion(entrega.nuevaEntrega.anio) }}
          <div class="text-h6">Adjunta todo lo relacionado {{ texto.adjunto }}</div> 
          <div v-if="mdvSeleccionado || hitosSeleccionados">
            <p>
              Adjunta todos los documentos necesarios conformen el medio de
              verificación "{{ texto.nombre }}". Éstos se subirán a
              Google Drive
            </p>
            <Picker :baseDir="texto.dirGoogle" />
            <!--<Picker :baseDir="mdvSeleccionado.dirGoogle" />-->
            <div
              v-if="entrega.adjuntosNuevaEntrega"
              class="q-pa-md"
              style="max-width: 400px"
            >
              <div class="text-weight-bold">
                Documentos subidos a Google Drive:
              </div>
              <q-list
                bordered
                v-for="item in entrega.adjuntosNuevaEntrega"
                :key="item.id"
              >
                <q-item clickable v-ripple @click="clickAdjunto(item)">
                  <q-item-section>
                    <q-item-label caption>{{ item.name }}</q-item-label>
                    <q-item-label caption>{{ item.type }}</q-item-label>
                  </q-item-section>
                  <q-item-section avatar>
                    <q-icon color="primary" name="file_download" />
                  </q-item-section>
                </q-item>
              </q-list>
            </div>
          </div>
        </q-step>
        <template v-slot:navigation>
          <q-stepper-navigation class="tarjetaAmarilla">
            <div class="row justify-end">
              <q-btn
                color="btnCancelar"
                label="Cancelar"
                class="q-ml-sm"
                @click="clicCancelar"
              />
              <q-btn
                v-if="step > 1"
                color="btnVolver"
                @click="$refs.stepper.previous()"
                label="Volver"
                class="q-ml-sm"
              />
              <q-btn
                v-if="step < 3"
                @click="$refs.stepper.next()"
                color="btnContinuar"
                label="Continuar"
                class="q-ml-sm"
                :disable="hitosSeleccionados.length === 0 ? true : false"
              />
              <q-btn
                v-if="step == 3"
                @click="submitEntregable"
                color="primary"
                label="Finalizar"
                class="q-ml-sm"
                :disable="!entrega.adjuntosNuevaEntrega"
              />
            </div>
          </q-stepper-navigation>
        </template>
      </q-stepper>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted, onUnmounted } from "vue";
import { useStore } from "vuex";
import { useRouter } from "vue-router";
import Picker from "src/components/Picker.vue";
import PopupCancelarNuevaEntrega from "src/components/PopupCancelarNuevaEntrega.vue";

export default {
  components: {
    Picker,
    PopupCancelarNuevaEntrega,
  },
  methods:{
    defineSeleccion (anio) {
      if (anio == 2022){
        return "multiple";
      }else if (anio == 2023) {
        return "single";
      }
    },
    defineDescripcion (anio) {
      if (anio == 2022){
        this.texto.adjunto = "al MDV.";
        this.texto.nombre = this.mdvSeleccionado.nombre;
        this.texto.dirGoogle = this.mdvSeleccionado.dirGoogle;
      }else if(anio == 2023) {
        this.texto.adjunto = "a las Actividades."
        this.texto.nombre = this.hitosSeleccionados.nombre;
        this.texto.dirGoogle = this.hitosSeleccionados.dirGoogle;
      }
      
    },
  },
  setup() {
    const store = useStore();
    const router = useRouter();
    const entrega = computed(() => store.state.entrega);
    const producto = computed(() => store.state.producto);
    const accion = computed(() => store.state.accion);
    const usuario = computed(() => store.state.usuarix);
    const funciones = ref([]);
    const texto = ref({});
    const hitosSeleccionados = ref([]);
    const mdvSeleccionado = ref(null);
    const notasAdicionales = ref("");
    const nivelAvance = ref(0);
    const descripcionMDV = ref("");
    const mostrarPopupCancelar = ref(false);
    const respuestaPopupCancelar = ref("");
    const clickAdjunto = (item) => {
      window.open(item.url);
    };

    const submitEntregable = () => {
      let valorMdv = "";
      if (mdvSeleccionado.value != null) {
        valorMdv = mdvSeleccionado.value.id
      }
      
      if (!Array.isArray(hitosSeleccionados.value)){
        hitosSeleccionados.value = [hitosSeleccionados.value];
      }

      const nuevoProducto = {
        usuario: usuario.value.usuario.id,
        mdv: valorMdv,
        hitos: hitosSeleccionados.value.map((item) => {
          return item.id;
        }),
        descripcion: descripcionMDV.value,
        adjuntos: entrega.value.adjuntosNuevaEntrega,
      };
      store.dispatch("producto/postProducto", nuevoProducto);
    };
    onMounted(() => {
      if (entrega.value.nuevaEntrega) {
        store.dispatch("accion/reqMDVPorAccion", entrega.value.nuevaEntrega.id);
        store.dispatch(
          "accion/reqHitosPorAccion",
          entrega.value.nuevaEntrega.id
        );
      }
    });
    onUnmounted(() => {
      store.dispatch("verificador/limpiaNuevoVerificador");
      store.dispatch("producto/limpiaNuevoProducto");
      store.dispatch("entrega/limpiaAdjuntos");
    });

    return {
      texto,
      clickAdjunto,
      entrega,
      producto,
      accion,
      funciones,
      hitosSeleccionados,
      mdvSeleccionado,
      notasAdicionales,
      nivelAvance,
      descripcionMDV,
      mostrarPopupCancelar,
      respuestaPopupCancelar,
      handlerPopupCancelar: (respuesta) => {
        mostrarPopupCancelar.value = false;
        if (respuesta == "guarda") {
          submitEntregable();
          router.push("acciones");
        } else if (respuesta == "sale") {
          router.push("acciones");
        } else {
          // se hace nada
        }
      },
      submitEntregable,
      enviaAlLider: () => {        
        store.dispatch("entrega/workflowEnviaAlLider", {
          entrega_id: producto.value.nuevoProducto.id,
          entrega_tipo: "producto",
        });
      },
      step: ref(1),
      clicCancelar: () => {
        if (descripcionMDV.value.trim().length > 0){
          mostrarPopupCancelar.value = true;
        }
        else
          router.push("acciones");
          // router.push(
          //   accion.value.referenciaSubirEntregable == "AccionesPOA"
          //     ? "acciones"
          //     : "accionesPMI"
          // );
      },
    };
  },
};
</script>

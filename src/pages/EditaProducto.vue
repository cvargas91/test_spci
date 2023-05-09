<template>
  <div class="q-pa-md">
    <PopupCancelarNuevaEntrega
      :mostrar="mostrarPopupCancelar"
      @update:mostrar="mostrarPopupCancelar = $event"
      @respuestaPopup="handlerPopupCancelar"
    />

    <div v-if="producto.productoModificado">
      <div class="text-h6">¡Felicitaciones!</div>
      <p>Se ha actualizado el producto</p>
      <q-btn
        label="Ir a la bandeja de entregas"
        to="bandejaEntregas"
        color="primary"
      />
    </div>

    <div v-else-if="entrega.aModificar">
      <div class="text-h6">
        Actualizando {{ entrega.aModificar.entrega.descripcion }}
      </div>

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
          bg-color="blue"
        >
          <!--          class="tarjetaAmarilla"  -->
          <div class="text-h6">
            Seleccione un Medio de Verificación (MDV) de
            {{ id_uaysenAccion }} y a los hitos
            que cumple con esta entrega
          </div>
          <!--<div v-if="accion.value.MDVs.length">-->
          <div v-if="accion.MDVs.length">
            <q-select
              label="Medio de Verificación"
              v-model="mdvSeleccionado"
              :options="accion.MDVs"
            />
            <!--:options="accion.value.MDVs"-->
          </div>

          <div v-else>
            <q-banner class="bg-primary text-white">
              No hay Medios de Verificación asociados a la acción
              {{ id_uaysenAccion }}. Contacta a
              UPCI con los antecedentes necesarios para revisar el caso
            </q-banner>
          </div>

          <!--<div v-if="accion.value.hitos.length">-->            
          <div v-if="accion.hitos.length">
            <q-select
              label="Hitos"
              use-chips
              stack-label
              :multiple="defineSeleccion(entrega.aModificar.anio)"
              v-model="hitosSeleccionados"
              :options="accion.hitos"
              option-value="id"
              option-label="nombre"
            />
          </div>

          <div v-else>
            <q-banner class="bg-primary text-white">
              No hay hitos asociados a la acción #{{
                entrega.aModificar.id_accion
              }}. Contacta a UPCI para revisar el caso
            </q-banner>
          </div>
        </q-step>

        <q-step
          :name="2"
          title="Describe la entrega"
          caption="Optional"
          icon="create_new_folder"
          :done="step > 2"
        >
          <!--class="tarjetaAmarilla"-->
          <div class="text-h6">Describe la actual entrega</div>
          <q-input
            v-model="descripcionMDV"
            filled
            type="textarea"
            placeholder="Explica los avances más importantes que se cumplen con esta entrega. Esto permitirá acelerar el proceso de revisión por parte del equipo UPCI"
          />
        </q-step>

        <q-step :name="3" title="Adjunta" icon="assignment">
          <!--class="tarjetaAmarilla"-->
          {{ defineDescripcion(entrega.aModificar.anio) }}
          <div class="text-h6">Adjunta todo lo relacionado al MDV</div>

          <div v-if="mdvSeleccionado || hitosSeleccionados">
            <p>
              Adjunta todos los documentos necesarios conformen el medio de
              verificación "{{ texto.nombre }}". Éstos
              se subirán a Google Drive
            </p>

            <div class="text-weight-bold">
              Documentos subidos a Google Drive:
            </div>
            <div v-if="entrega.adjuntosEdicionEntrega">
              <q-list
                v-for="item in entrega.adjuntosEdicionEntrega"
                :key="item.id"
                bordered
                class="rounded-borders"
                style="max-width: 600px"
              >
                <q-item>
                  <q-item-section top class="col-2 gt-sm">
                    <q-item-label class="q-mt-sm">
                      {{ item.name }}
                    </q-item-label>
                    <q-item-section top side align="right">
                      <div class="text-grey-8 q-gutter-xs">
                        <q-btn
                          class="gt-xs"
                          size="12px"
                          flat
                          dense
                          round
                          icon="delete"
                          @click="eliminarAdjunto(item)"
                        />
                        <q-btn
                          type="a"
                          target="_blank"
                          :href="item.downloadUrl"
                          class="gt-xs"
                          size="12px"
                          flat
                          dense
                          round
                          icon="download"
                        />
                      </div>
                    </q-item-section>
                  </q-item-section>
                </q-item>
              </q-list>
            </div>
            <q-separator color="blue" inset />
            <!--<Picker :baseDir="entrega.aModificar.entrega.mdv.dirGoogle" />-->
            <Picker :baseDir="texto.dirGoogle" />
          </div>
        </q-step>
        <template v-slot:navigation>
          <q-stepper-navigation>
            <!--class="tarjetaAmarilla"-->
            <q-btn
              v-if="step == 3"
              @click="submitEdicionProducto"
              color="brown-5"
              label="Finalizar"
              :disable="!entrega.adjuntosEdicionEntrega"
            />
            <q-btn
              v-if="step < 3"
              @click="$refs.stepper.next()"
              color="btnContinuar"
              label="Continuar"
              :disable="hitosSeleccionados.length === 0 ? true : false"
            />
            <q-btn
              v-if="step > 1"
              flat
              color="btnVolver"
              @click="$refs.stepper.previous()"
              label="Volver"
              class="q-ml-sm"
            />
            <q-btn
              color="btnCancelar"
              label="Cancelar"
              class="q-ml-sm"
              @click="clicCancelar"
            />
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
    PopupCancelarNuevaEntrega
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
    const id_accion = entrega.value.aModificar.entrega.mdv ? entrega.value.aModificar.entrega.mdv.accion.id : entrega.value.aModificar.entrega.hitos[0].accion.id;
    const id_uaysenAccion = entrega.value.aModificar.entrega.mdv ? entrega.value.aModificar.entrega.mdv.accion.id_uaysen : entrega.value.aModificar.entrega.hitos[0].accion.id_uaysen;
    const texto = ref({});
    const usuario = computed(() => store.state.usuarix);
    const adjuntosActuales = entrega.value.aModificar.entrega.adjuntos;
    const hitosSeleccionados = ref(entrega.value.aModificar.entrega.hitos[0]);
    const mostrarPopupCancelar = ref(false);
    const respuestaPopupCancelar = ref("");
    const mdvSeleccionado = ref(entrega.value.aModificar.entrega.mdv);
    const descripcionMDV = ref(entrega.value.aModificar.entrega.descripcion);

    const clickAdjunto = (item) => {
      window.open(item.url);
    };
    const submitEdicionProducto= () => {
        let valorMdv = "";
        if (mdvSeleccionado.value != null) {
          valorMdv = mdvSeleccionado.value.id
        }
      
        if (!Array.isArray(hitosSeleccionados.value)){
          hitosSeleccionados.value = [hitosSeleccionados.value];
        }

        const productoModificado = {
          id: entrega.value.aModificar.entrega.id,
          usuario: usuario.value.usuario.id,
          mdv: valorMdv,
          hitos: hitosSeleccionados.value.map((item) => {
            return item.id;
          }),
          descripcion: descripcionMDV.value,
          adjuntos: entrega.value.adjuntosEdicionEntrega,
        };
        
        store.dispatch("entrega/setModificaProducto", productoModificado);
        router.push("bandejaEntregas");
    };
    onMounted(() => {
      store.dispatch("entrega/limpiaAdjuntosEdicion");
      if (entrega.value.aModificar) {
        store.dispatch("accion/reqMDVPorAccion", id_accion);
        store.dispatch("accion/reqHitosPorAccion", id_accion);

        if(adjuntosActuales){
          store.dispatch("entrega/setAdjuntosEdicionEntrega", adjuntosActuales);
        } else{
          console.log("Entrega sin adjuntos");
        }
      }
    });

    return {
      texto,
      id_uaysenAccion,
      entrega,
      clickAdjunto,
      producto,
      accion,
      hitosSeleccionados,
      //mdvSeleccionado: ref(mdvSeleccionado.value.nombre),
      mdvSeleccionado: ref(mdvSeleccionado.value ? mdvSeleccionado.value.nombre : ' - '),
      descripcionMDV,
      mostrarPopupCancelar,
      respuestaPopupCancelar,
      eliminarAdjunto(item) {
        store.dispatch("entrega/setAdjuntosEdicionEntrega", [item]);
      },
      step: ref(1),
      handlerPopupCancelar: (respuesta) => {
        mostrarPopupCancelar.value = false;
        if (respuesta == "guarda") {
          submitEdicionProducto();
          router.push("bandejaEntregas");
        } else if (respuesta == "sale") {
          router.push("bandejaEntregas");
        } else {
          // se hace nada
        }
      },
      submitEdicionProducto,
      clicCancelar: () => {
        mostrarPopupCancelar.value = true;
      },
    };
  },
};
</script>

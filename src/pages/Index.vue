<template>
  <q-page>
    <div class="q-pa-md" v-if="usuario.perfil">
      <div class="text-textoAzul text-h6 q-ml-lg">
        <b>¡Hola {{ usuario.nombre }}, Bienvenid@!</b>
      </div>
      <div class="q-pa-md">
        <div class="q-gutter-md">
          <q-carousel
            v-model="slide"
            transition-prev="scale"
            transition-next="scale"
            swipeable
            animated
            control-color="white"
            navigation
            padding
            arrows
            height="350px"
            class="shadow-1 rounded-borders"
          >
            <q-carousel-slide
              name="cero"
              class="bg-grey-4 text-white column no-wrap flex-center"
            >
              <iframe
                frameBorder="0"
                src="https://drive.google.com/file/d/1jATqd9Jdi_W4Xresv_O2W0tb5iMVI0Mc/preview"
                allow="autoplay"
                style="min-height: inherit; min-width: 80%"
              ></iframe>
            </q-carousel-slide>

            <q-carousel-slide
              name="uno"
              class="bg-teal-14 text-white column no-wrap flex-center"
            >
              <q-icon name="settings_system_daydream" size="56px" />
              <div class="q-mt-md text-center">
                <b>Colabora</b> es una plataforma de apoyo al logro de
                compromisos institucionales asociada a la estrategia
                universitaria
              </div>
            </q-carousel-slide>
            <q-carousel-slide
              name="dos"
              class="bg-cyan-7 text-white column no-wrap flex-center"
            >
              <q-icon name="run_circle" size="56px" />
              <div class="q-mt-md text-center">
                En el contexto del desarrollo y el quehacer institucional, se
                entenderá por <b>acción</b> como cualquier conjunto coordinado
                de actividades, las cuales son gestadas y desarrolladas desde y
                por actores vinculados a la Institución, y que tienen como
                resultado uno o varios productos que tributan a implementar la
                estrategia institucional
              </div>
            </q-carousel-slide>
            <q-carousel-slide
              name="tres"
              class="bg-orange-8 text-white column no-wrap flex-center"
            >
              <q-icon name="construction" size="56px" />
              <div class="q-mt-md text-center">
                Las <b>funciones</b> corresponden a tareas desarrolladas en el
                marco de las responsabilidades de los actores involucrados en la
                iniciativa, que a través de su realización tributan al
                cumplimiento del objetivo planteado para la iniciativa
              </div>
            </q-carousel-slide>
            <q-carousel-slide
              name="cuatro"
              class="bg-green-6 text-white column no-wrap flex-center"
            >
              <q-icon name="event_available" size="56px" />
              <div class="q-mt-md text-center">
                Los <b>hitos</b> corresponden a eventos de relevancia durante el
                desarrollo de la acción, que se transforman en objeto de
                cumplimiento en su ejecución y que dan cuenta del alcance del
                objetivo planteado
              </div>
            </q-carousel-slide>
            <q-carousel-slide
              name="final"
              class="bg-pink-7 text-white column no-wrap flex-center"
            >
              <q-icon name="favorite" size="56px" />
              <div class="q-mt-md text-center">
                <b>¡Gracias por usar Colabora!</b>
              </div>
            </q-carousel-slide>
          </q-carousel>
        </div>
      </div>
    </div>
  </q-page>
</template>

<script>
import { ref, computed, onMounted, defineComponent } from "vue";
import { useStore } from "vuex";
import Plotly from "src/components/Plotly.vue";

export default defineComponent({
  components: {
    Plotly,
  },
  setup() {
    const store = useStore();
    return {
      usuario: computed(() => store.state.usuarix.usuario),
      slide: ref("cero"),
    };
  },
});
</script>

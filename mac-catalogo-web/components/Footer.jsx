export default function Footer() {
  return (
    <footer className="border-t border-neutral-200 bg-white mt-10 text-xs text-neutral-700">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 py-8">
        <div className="grid gap-6 md:grid-cols-4">
          <div className="space-y-3">
            <img
              src="/assets/mac.svg"
              alt="MAC Lima"
              className="h-10 w-auto"
            />
          </div>

          <div>
            <h3 className="font-semibold mb-2 text-sm">Más sobre el MAC Lima</h3>
            <ul className="space-y-1">
              <li>Publicaciones</li>
              <li>Archivo MAC Lima</li>
              <li>Centro de documentación</li>
              <li>Oportunidades laborales</li>
              <li>Eventos privados</li>
            </ul>
          </div>

          <div>
            <h3 className="font-semibold mb-2 text-sm">Horario</h3>
            <p>Abierto: Martes a domingo de 10 a 7 p.m.</p>
            <p>*Sujeto a cambios sin previo aviso.</p>
          </div>

          <div>
            <h3 className="font-semibold mb-2 text-sm">Contacto</h3>
            <p>Museo de Arte Contemporáneo de Lima (MAC Lima)</p>
            <p>Av. Grau 1511, Barranco, Lima - Perú</p>
            <p>(01) 513-9000</p>
            <p>contacto@maclima.pe</p>
          </div>
        </div>

        <div className="text-center text-[11px] mt-6 text-neutral-500">
          Políticas de privacidad | MAC Lima © 2019 | All Rights Reserved
        </div>
      </div>
    </footer>
  );
}

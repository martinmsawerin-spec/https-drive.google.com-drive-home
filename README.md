# Mis Gastos

Aplicación web simple para registrar gastos diarios de forma rápida y clasificarlos por categoría.

## Características

- Registro rápido: monto, categoría (con íconos), nota opcional y fecha.
- 8 categorías predefinidas: Comida, Transporte, Vivienda, Salud, Ocio, Compras, Educación, Otros.
- Resumen de gastos de hoy y del mes actual.
- Historial de gastos agrupado por día, con opción de eliminar.
- Estadísticas por categoría con navegación entre meses.
- Sin backend ni instalación: todo se guarda en el navegador (`localStorage`).
- Funciona offline y en móvil (diseño responsivo, pensado para uso rápido con el pulgar).

## Uso

Abre `index.html` en cualquier navegador. No requiere servidor, build ni dependencias.

También puedes servirlo con cualquier servidor estático, por ejemplo:

```bash
python3 -m http.server 8000
```

y luego visitar `http://localhost:8000`.

## Notas

- Los datos se guardan localmente en el navegador que uses (localStorage), por lo que no se sincronizan entre dispositivos.
- El símbolo de moneda por defecto es `$`; puede ajustarse cambiando la clave `currency_symbol_v1` en `localStorage` si se desea.

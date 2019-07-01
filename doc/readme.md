# Documentación

**Nombre** | **Grupo** | **Github**
--|--|--
Ernesto Estevanell Valladares | C412 | [@eestevanell](https://github.com/EEstevanell)
Liliette Chiu Rodríguez | C412 | [@liliettechiu](https://github.com/LilietteChiu)
Alejandro Ojeda Fernández | C412 | [@alejof](https://github.com/Alejof)

## Requisitos

- Tener una instalación de Python v3.6 o superior (Se utilizan anotaciones).
- Tener una instalación del paquete `ply` de Python.
  
## Ejecución y Opciones
El compilador implementado cuenta con dos opciones para su ejecución:
- Opción simple (compila un `cool-code`)
  ```
  python CoolCompilerX.py `<cool-code>` [output-file-name]
  ```
- Opción para pruebas múltiples (Dado un directorio (testing-directory) busca archivos `cool-code` de manera recursiva y los compila)
  ```
  python CoolCompilerX.py -t [testing-directory]
  ```

## Repositorio de GitHub
Aquí se ofrece un link al repositorio del proyecto en GitHub:
- [@Cool-Compiler-X](https://github.com/matcom-compilers-2019/cool-compiler-estevanell-liliette-ale-ojeda)

### Estructura del reporte
El compilador se encuentra separado en los siguentes módulos:
- `CoolCompilerX` (Módulo principal, Contiene la definición del compilador en si, manejando el proceso de compilación.)
- `lexer`
- `parsing`
- `scope`
- `semantics`
- `CILgenerator`
- `MIPSgenerator`
- `settings`
- `Cool\ast`
- `CIL\ast`
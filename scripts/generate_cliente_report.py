from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile
import xml.etree.ElementTree as ET


NS_URI = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
NS = {"w": NS_URI}
W = f"{{{NS_URI}}}"

ET.register_namespace("w", NS_URI)


def para_text(paragraph):
    return "".join(text_node.text or "" for text_node in paragraph.findall(".//w:t", NS)).strip()


def create_run(text, bold=False, italic=False, size=None, color=None):
    run = ET.Element(W + "r")
    run_properties = ET.SubElement(run, W + "rPr")

    if bold:
        ET.SubElement(run_properties, W + "b")
    if italic:
        ET.SubElement(run_properties, W + "i")
    if color:
        color_tag = ET.SubElement(run_properties, W + "color")
        color_tag.set(W + "val", color)
    if size:
        size_tag = ET.SubElement(run_properties, W + "sz")
        size_tag.set(W + "val", str(size))
        size_cs_tag = ET.SubElement(run_properties, W + "szCs")
        size_cs_tag.set(W + "val", str(size))

    text_tag = ET.SubElement(run, W + "t")
    if text.startswith(" ") or text.endswith(" ") or "  " in text:
        text_tag.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
    text_tag.text = text
    return run


def create_paragraph(
    texts=None,
    style=None,
    align=None,
    spacing_before=None,
    spacing_after=None,
):
    paragraph = ET.Element(W + "p")
    paragraph_properties = ET.SubElement(paragraph, W + "pPr")

    if style:
        style_tag = ET.SubElement(paragraph_properties, W + "pStyle")
        style_tag.set(W + "val", style)

    if align:
        align_tag = ET.SubElement(paragraph_properties, W + "jc")
        align_tag.set(W + "val", align)

    if spacing_before is not None or spacing_after is not None:
        spacing_tag = ET.SubElement(paragraph_properties, W + "spacing")
        if spacing_before is not None:
            spacing_tag.set(W + "before", str(spacing_before))
        if spacing_after is not None:
            spacing_tag.set(W + "after", str(spacing_after))

    if texts:
        for entry in texts:
            paragraph.append(
                create_run(
                    text=entry["text"],
                    bold=entry.get("bold", False),
                    italic=entry.get("italic", False),
                    size=entry.get("size"),
                    color=entry.get("color"),
                )
            )

    return paragraph


def create_page_break():
    paragraph = ET.Element(W + "p")
    run = ET.SubElement(paragraph, W + "r")
    br = ET.SubElement(run, W + "br")
    br.set(W + "type", "page")
    return paragraph


def create_bullet(text):
    return create_paragraph(
        texts=[{"text": "\u2022 " + text}],
        style="ListParagraph",
        spacing_after=120,
    )


def main():
    source_path = list(Path(r"C:\Users\nicon\Downloads").glob("PI Pr*3.docx"))[0]
    output_path = Path(r"C:\Users\nicon\OneDrive\Desktop\Universidad\ProyectoPI\PI Practica3 - cliente final.docx")

    with ZipFile(source_path, "r") as source_zip:
        files = {name: source_zip.read(name) for name in source_zip.namelist()}

    document_root = ET.fromstring(files["word/document.xml"])
    body = document_root.find("w:body", NS)

    original_paragraphs = [node for node in body if node.tag == W + "p"]
    group_names = [para_text(node) for node in original_paragraphs[5:11]]
    acta_1 = [para_text(node) for node in original_paragraphs[29:34]]
    sect_pr = [node for node in body if node.tag == W + "sectPr"][-1]

    for node in list(body):
        body.remove(node)

    body.append(
        create_paragraph(
            texts=[{"text": "Programaci\u00f3n en Internet 2025/26", "size": 22, "color": "1F3B64"}],
            align="center",
            spacing_after=240,
        )
    )
    body.append(
        create_paragraph(
            texts=[{"text": "PR\u00c1CTICA 03", "bold": True, "size": 36, "color": "1F3B64"}],
            align="center",
            spacing_after=120,
        )
    )
    body.append(
        create_paragraph(
            texts=[{"text": "Subsonic Festival", "bold": True, "size": 28, "color": "375D81"}],
            align="center",
            spacing_after=120,
        )
    )
    body.append(
        create_paragraph(
            texts=[{"text": "Memoria de desarrollo del back-end - Perfil Cliente", "italic": True, "size": 22}],
            align="center",
            spacing_after=360,
        )
    )
    body.append(
        create_paragraph(
            texts=[{"text": "Asignatura: Programaci\u00f3n en Internet", "size": 22}],
            align="center",
            spacing_after=120,
        )
    )
    body.append(
        create_paragraph(
            texts=[{"text": "Curso acad\u00e9mico: 2025/26", "size": 22}],
            align="center",
            spacing_after=120,
        )
    )
    body.append(
        create_paragraph(
            texts=[{"text": "Fecha: 13 de marzo de 2026", "size": 22}],
            align="center",
            spacing_after=360,
        )
    )
    body.append(
        create_paragraph(
            texts=[{"text": "Integrantes del grupo", "bold": True, "size": 24, "color": "1F3B64"}],
            align="center",
            spacing_after=180,
        )
    )

    for name in group_names:
        body.append(
            create_paragraph(
                texts=[{"text": name, "size": 22}],
                align="center",
                spacing_after=60,
            )
        )

    body.append(create_page_break())

    body.append(create_paragraph(texts=[{"text": "\u00cdNDICE"}], style="Heading2", spacing_after=240))
    body.append(create_paragraph(texts=[{"text": "1. Introducci\u00f3n"}], style="Normal", spacing_after=120))
    body.append(create_paragraph(texts=[{"text": "2. Parte desarrollada: perfil Cliente"}], style="Normal", spacing_after=120))
    body.append(create_paragraph(texts=[{"text": "3. Lista de end-points construidos y documentaci\u00f3n asociada"}], style="Normal", spacing_after=120))
    body.append(create_paragraph(texts=[{"text": "4. Anexo: actas de reuni\u00f3n"}], style="Normal", spacing_after=120))

    body.append(create_page_break())

    body.append(create_paragraph(texts=[{"text": "1. Introducci\u00f3n"}], style="Heading2", spacing_after=180))
    body.append(
        create_paragraph(
            texts=[
                {
                    "text": "La presente memoria recoge el trabajo desarrollado en la Pr\u00e1ctica 03 de la asignatura Programaci\u00f3n en Internet sobre el caso de estudio Subsonic Festival. En esta fase del proyecto se ha completado la implementaci\u00f3n del back-end correspondiente al perfil Cliente, manteniendo el mismo repositorio utilizado previamente para el front-end y asegurando el despliegue completo de la aplicaci\u00f3n en localhost."
                }
            ],
            style="Normal",
            spacing_after=180,
        )
    )
    body.append(
        create_paragraph(
            texts=[
                {
                    "text": "El desarrollo realizado se ha ajustado a los requisitos establecidos en el enunciado de la pr\u00e1ctica. En concreto, se ha utilizado Python con FastAPI como base del servicio, se ha mantenido la arquitectura basada en MVC, DAO, Factory y DTO, y se ha respetado la estructura de clases del proyecto de ejemplo mostrado en clase."
                }
            ],
            style="Normal",
            spacing_after=180,
        )
    )
    body.append(
        create_paragraph(
            texts=[
                {
                    "text": "El objetivo principal de esta parte del trabajo ha sido dejar completamente cerrado el perfil Cliente antes de comenzar la integraci\u00f3n del resto de perfiles de la aplicaci\u00f3n. Para ello se ha completado la conexi\u00f3n entre front-end y back-end en todas las vistas del Cliente y se ha verificado su funcionamiento de extremo a extremo."
                }
            ],
            style="Normal",
            spacing_after=180,
        )
    )

    body.append(create_paragraph(texts=[{"text": "2. Parte desarrollada: perfil Cliente"}], style="Heading2", spacing_after=180))
    body.append(create_paragraph(texts=[{"text": "2.1 Arquitectura utilizada"}], style="Heading3", spacing_after=120))
    body.append(
        create_paragraph(
            texts=[
                {
                    "text": "El back-end se ha desarrollado en Python utilizando FastAPI como framework para exponer la API REST. La capa controller recibe las peticiones HTTP y devuelve las respuestas al front-end; la capa model centraliza la l\u00f3gica de negocio; la capa DAO gestiona el acceso a la persistencia local; la factor\u00eda LocalDAOFactory encapsula la creaci\u00f3n de los DAOs; y los DTOs permiten transportar la informaci\u00f3n entre capas de forma estructurada."
                }
            ],
            style="Normal",
            spacing_after=180,
        )
    )
    body.append(
        create_paragraph(
            texts=[
                {
                    "text": "La persistencia actual se ha resuelto mediante archivos JSON almacenados en la carpeta backend/data. Para la parte Cliente se utilizan principalmente users.json, tickets.json y purchaseOptions.json. Esta soluci\u00f3n permite disponer de un prototipo funcional sin introducir todav\u00eda una base de datos relacional, manteniendo una separaci\u00f3n clara de responsabilidades entre las distintas capas del sistema."
                }
            ],
            style="Normal",
            spacing_after=180,
        )
    )

    body.append(create_paragraph(texts=[{"text": "2.2 Funcionalidades completadas"}], style="Heading3", spacing_after=120))
    body.append(create_bullet("Login funcional conectado con el end-point POST /login."))
    body.append(create_bullet("Listado de entradas del usuario conectado con GET /tickets/{id_usuario}."))
    body.append(create_bullet("Pantalla de detalle conectada con GET /ticket/{ticket_id}."))
    body.append(create_bullet("Cancelaci\u00f3n de entradas conectada con PUT /ticket/cancel/{ticket_id}."))
    body.append(create_bullet("Compra de entradas conectada con GET /purchase/options y POST /purchase."))
    body.append(create_bullet("Perfil del usuario conectado con GET /profile/{id_usuario} y PUT /profile/{id_usuario}."))

    body.append(create_paragraph(texts=[{"text": "2.3 Integraci\u00f3n entre front-end y back-end"}], style="Heading3", spacing_after=120))
    body.append(
        create_paragraph(
            texts=[
                {
                    "text": "En el front-end se ha mantenido el uso de HTML, CSS y JavaScript puro, sin incorporar frameworks adicionales. Las vistas login.html, tickets.html, ticket-detail.html, purchase.html y profile.html consumen la API REST mediante fetch y quedan servidas tambi\u00e9n desde FastAPI, lo que permite ejecutar toda la aplicaci\u00f3n desde localhost con un \u00fanico arranque del servidor."
                }
            ],
            style="Normal",
            spacing_after=180,
        )
    )
    body.append(
        create_paragraph(
            texts=[
                {
                    "text": "Una mejora importante del trabajo realizado ha sido la migraci\u00f3n del perfil del usuario, que inicialmente guardaba los cambios solo en localStorage. En la versi\u00f3n actual el perfil se consulta y actualiza a trav\u00e9s del back-end, quedando persistido correctamente en users.json. Adem\u00e1s, la pantalla de compra ya no depende de datos hardcodeados en el front-end, ya que los eventos y tipos de pase disponibles se obtienen desde el servidor."
                }
            ],
            style="Normal",
            spacing_after=180,
        )
    )
    body.append(
        create_paragraph(
            texts=[
                {
                    "text": "Con esta implementaci\u00f3n, la parte Cliente puede considerarse funcionalmente cerrada dentro del alcance de la pr\u00e1ctica. Todas las vistas asociadas a este perfil est\u00e1n conectadas con el back-end y se han probado correctamente en localhost, cubriendo el flujo completo de autenticaci\u00f3n, consulta de entradas, detalle, cancelaci\u00f3n, compra y edici\u00f3n de perfil."
                }
            ],
            style="Normal",
            spacing_after=180,
        )
    )

    body.append(create_paragraph(texts=[{"text": "3. Lista de end-points construidos y documentaci\u00f3n asociada"}], style="Heading2", spacing_after=180))
    body.append(
        create_paragraph(
            texts=[
                {
                    "text": "A continuaci\u00f3n se recoge la relaci\u00f3n de end-points implementados para la parte Cliente, junto con una descripci\u00f3n resumida de su finalidad dentro del sistema:"
                }
            ],
            style="Normal",
            spacing_after=180,
        )
    )
    body.append(create_bullet("POST /login. Autentica al usuario a partir de su correo electr\u00f3nico y contrase\u00f1a, y devuelve sus datos p\u00fablicos."))
    body.append(create_bullet("GET /profile/{id_usuario}. Recupera el perfil del usuario autenticado para mostrarlo en la vista de perfil y en el panel lateral de tickets."))
    body.append(create_bullet("PUT /profile/{id_usuario}. Actualiza nombre, correo electr\u00f3nico, direcci\u00f3n y avatar del cliente, persistiendo los cambios en el servidor."))
    body.append(create_bullet("GET /tickets/{id_usuario}. Devuelve el listado de entradas asociadas a un usuario concreto."))
    body.append(create_bullet("GET /ticket/{ticket_id}. Recupera la informaci\u00f3n detallada de una entrada determinada."))
    body.append(create_bullet("GET /purchase/options. Proporciona al front-end los eventos y tipos de pase disponibles en la pantalla de compra."))
    body.append(create_bullet("PUT /ticket/cancel/{ticket_id}. Cambia el estado de una entrada concreta a Cancelada."))
    body.append(create_bullet("POST /purchase. Registra la compra de una o varias entradas nuevas y genera los tickets correspondientes en la persistencia JSON."))
    body.append(
        create_paragraph(
            texts=[
                {
                    "text": "Estos end-points permiten cubrir de forma completa el flujo funcional del perfil Cliente y sirven como base estable para la posterior integraci\u00f3n de los perfiles Visitante y Proveedor."
                }
            ],
            style="Normal",
            spacing_after=180,
        )
    )

    body.append(create_paragraph(texts=[{"text": "4. Anexo: actas de reuni\u00f3n"}], style="Heading2", spacing_after=180))
    body.append(create_paragraph(texts=[{"text": "Acta 1"}], style="Heading3", spacing_after=120))
    for line in acta_1[1:]:
        body.append(create_paragraph(texts=[{"text": line}], style="Normal", spacing_after=90))

    body.append(create_paragraph(texts=[{"text": "Acta 2"}], style="Heading3", spacing_before=180, spacing_after=120))
    body.append(
        create_paragraph(
            texts=[
                {
                    "text": "Fecha y Hora: [Completar por el grupo con la fecha y hora reales de la reuni\u00f3n de cierre de Cliente]."
                }
            ],
            style="Normal",
            spacing_after=90,
        )
    )
    body.append(create_paragraph(texts=[{"text": "Asistentes: [Completar por el grupo]."}], style="Normal", spacing_after=90))
    body.append(
        create_paragraph(
            texts=[
                {
                    "text": "Contenido: Revisi\u00f3n y cierre de la parte Cliente del back-end de Subsonic Festival. Durante esta fase se verific\u00f3 la correcta integraci\u00f3n entre front-end y back-end para login, tickets, detalle de entrada, cancelaci\u00f3n, compra y perfil. Tambi\u00e9n se revis\u00f3 la persistencia en archivos JSON y la adecuaci\u00f3n de la arquitectura utilizada a los patrones MVC, DAO, Factory y DTO exigidos por la pr\u00e1ctica."
                }
            ],
            style="Normal",
            spacing_after=90,
        )
    )
    body.append(
        create_paragraph(
            texts=[
                {
                    "text": "Decisiones: Mantener Python con FastAPI como base del back-end, conservar la persistencia temporal en JSON para esta pr\u00e1ctica, dejar completamente cerrada la parte Cliente antes de abordar la integraci\u00f3n de los perfiles Visitante y Proveedor, y documentar los end-points implementados en el informe final."
                }
            ],
            style="Normal",
            spacing_after=120,
        )
    )

    body.append(create_paragraph(texts=[{"text": "Acta 3"}], style="Heading3", spacing_before=180, spacing_after=120))
    body.append(
        create_paragraph(
            texts=[
                {
                    "text": "Fecha y Hora: [Completar por el grupo con la fecha y hora reales de la reuni\u00f3n de entrega]."
                }
            ],
            style="Normal",
            spacing_after=90,
        )
    )
    body.append(create_paragraph(texts=[{"text": "Asistentes: [Completar por el grupo]."}], style="Normal", spacing_after=90))
    body.append(
        create_paragraph(
            texts=[
                {
                    "text": "Contenido: Revisi\u00f3n final de los entregables de la Pr\u00e1ctica 03 y comprobaci\u00f3n del estado del repositorio GitHub, de la memoria y del despliegue local."
                }
            ],
            style="Normal",
            spacing_after=90,
        )
    )
    body.append(
        create_paragraph(
            texts=[
                {
                    "text": "Decisiones: Designar al miembro del grupo encargado de realizar la entrega final en el campus virtual, comprobar que el proyecto puede ejecutarse en localhost y verificar que la lista de end-points implementados aparece correctamente documentada en la memoria."
                }
            ],
            style="Normal",
            spacing_after=90,
        )
    )
    body.append(
        create_paragraph(
            texts=[
                {
                    "text": "Miembro designado para la entrega: [Completar por el grupo]."
                }
            ],
            style="Normal",
            spacing_after=90,
        )
    )

    body.append(sect_pr)

    files["word/document.xml"] = ET.tostring(document_root, encoding="utf-8", xml_declaration=True)

    with ZipFile(output_path, "w", ZIP_DEFLATED) as output_zip:
        for name, data in files.items():
            output_zip.writestr(name, data)

    print(output_path)


if __name__ == "__main__":
    main()

import hashlib

from backend.model.dao.factory.localDAOFactory import LocalDAOFactory


class Model:
    def __init__(self):
        self.factory = LocalDAOFactory()
        self.user_dao = self.factory.get_user_dao()
        self.space_dao = self.factory.get_space_dao()
        self.application_dao = self.factory.get_application_dao()
        self.stats_dao = self.factory.get_stats_dao()

    def _sha256(self, value):
        return hashlib.sha256(value.encode("utf-8")).hexdigest()

    def _require_provider(self, id_usuario):
        user = self.user_dao.get_user_by_id(id_usuario)
        if not user:
            return None, "Usuario no encontrado"
        if user.rol != "PROVEEDOR":
            return None, "El usuario no pertenece al perfil Proveedor"
        return user, None

    def login(self, email, password):
        user = self.user_dao.get_user_by_email(email)
        if user and user.password == self._sha256(password):
            return user
        return None

    def get_provider_profile(self, id_usuario):
        user, error = self._require_provider(id_usuario)
        if error:
            return None, error
        return user.to_public_dict(), None

    def update_provider_profile(self, id_usuario, name, email, address, avatarUrl=None,
                                businessName=None, phone=None, biography=None, socialLinks=None):
        _, error = self._require_provider(id_usuario)
        if error:
            return None, error

        updated = self.user_dao.update_provider_profile(
            id_usuario=id_usuario,
            name=name,
            email=email,
            address=address,
            avatarUrl=avatarUrl,
            businessName=businessName,
            phone=phone,
            biography=biography,
            socialLinks=socialLinks,
        )
        if not updated:
            return None, "No se pudo actualizar el perfil"
        return updated.to_public_dict(), None

    def add_gallery_image(self, id_usuario, image_url):
        _, error = self._require_provider(id_usuario)
        if error:
            return None, error
        if not image_url:
            return None, "La URL de imagen es obligatoria"
        updated = self.user_dao.add_gallery_image(id_usuario, image_url)
        if not updated:
            return None, "No se pudo actualizar la galería"
        return updated.to_public_dict(), None

    def get_spaces(self, tipo=None, only_available=False):
        spaces = self.space_dao.get_spaces(tipo, only_available)
        return [space.to_dict() for space in spaces]

    def get_space_by_id(self, id_espacio):
        space = self.space_dao.get_space_by_id(id_espacio)
        if not space:
            return None
        return space.to_dict()

    def get_applications_by_provider(self, id_usuario):
        _, error = self._require_provider(id_usuario)
        if error:
            return None, error
        applications = self.application_dao.get_applications_by_provider(id_usuario)
        return [application.to_dict() for application in applications], None

    def create_application(self, id_proveedor, id_espacio, descripcion, categoria_servicio, portfolio_url=None):
        _, error = self._require_provider(id_proveedor)
        if error:
            return None, error

        space = self.space_dao.get_space_by_id(id_espacio)
        if not space:
            return None, "Espacio no encontrado"
        if not space.disponible:
            return None, "El espacio seleccionado no está disponible"
        if self.application_dao.has_open_request_for_space(id_proveedor, id_espacio):
            return None, "Ya existe una solicitud activa para este espacio"

        application = self.application_dao.create_application(
            id_proveedor=id_proveedor,
            id_espacio=id_espacio,
            descripcion=descripcion,
            categoria_servicio=categoria_servicio,
            portfolio_url=portfolio_url,
        )
        return application.to_dict(), None

    def get_provider_stats(self, id_usuario):
        _, error = self._require_provider(id_usuario)
        if error:
            return None, error
        pending = self.application_dao.count_by_state(id_usuario, "PENDIENTE")
        approved = self.application_dao.count_by_state(id_usuario, "APROBADA")
        rejected = self.application_dao.count_by_state(id_usuario, "RECHAZADA")
        stats = self.stats_dao.get_stats_by_provider(id_usuario, pending, approved, rejected)
        return stats.to_dict(), None

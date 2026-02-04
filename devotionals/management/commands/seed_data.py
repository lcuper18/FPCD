from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from devotionals.models import Category, Devotional
from materials.models import Material
from django.utils.text import slugify
from django.utils import timezone

User = get_user_model()

class Command(BaseCommand):
    help = 'Genera datos de prueba para Fe para Cada Día'

    def handle(self, *args, **options):
        self.stdout.write('🌱 Generando datos de prueba...\n')

        # Obtener o crear usuario admin
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@fecadadia.com',
                'is_staff': True,
                'is_superuser': True,
            }
        )
        if created:
            admin_user.set_password('admin123')
            admin_user.save()
            self.stdout.write(self.style.SUCCESS('✅ Usuario admin creado'))
        else:
            self.stdout.write('✓ Usuario admin ya existe')

        # Crear categorías
        categories_data = [
            {
                'name': 'Esperanza',
                'description': 'Reflexiones sobre la esperanza en Dios'
            },
            {
                'name': 'Fe',
                'description': 'Devocionales sobre la fe en tiempos difíciles'
            },
            {
                'name': 'Amor',
                'description': 'El amor de Dios y cómo amarnos los unos a los otros'
            },
            {
                'name': 'Sanidad',
                'description': 'Devocionales sobre sanidad física y emocional'
            },
            {
                'name': 'Propósito',
                'description': 'Descubriendo nuestro propósito en Dios'
            },
        ]

        categories = {}
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={
                    'slug': slugify(cat_data['name']),
                    'description': cat_data['description'],
                }
            )
            categories[cat_data['name']] = category
            if created:
                self.stdout.write(self.style.SUCCESS(f'✅ Categoría "{cat_data["name"]}" creada'))
            else:
                self.stdout.write(f'✓ Categoría "{cat_data["name"]}" ya existe')

        # Crear devocionales
        devotionals_data = [
            {
                'title': 'Confía en el Señor con todo tu corazón',
                'subtitle': 'Una reflexión sobre la confianza en Dios',
                'bible_verse': 'Proverbios 3:5-6',
                'bible_reference': 'Prov 3:5-6',
                'content': '''
                <h2>Reflexión del día</h2>
                <p>A veces nos encontramos en situaciones donde todo parece incierto. 
                Las circunstancias nos rodean como una tormenta, y no sabemos qué hacer. 
                Pero Dios nos invita a confiar en Él completamente.</p>
                
                <p>"Confía en el Señor con todo tu corazón, y no te apoyes en tu propio entendimiento. 
                Reconócelo en todos tus caminos, y él allanará tus sendas." (Proverbios 3:5-6)</p>
                
                <p>Esta es una promesa poderosa. No se nos pide que entendamos todo, 
                sino que confiemos en la sabiduría y bondad de Dios.</p>
                ''',
                'reflection': 'Reflexiona: ¿En qué áreas de tu vida necesitas aprender a confiar más en Dios?',
                'prayer': 'Señor, ayúdame a dejar mis preocupaciones en tus manos y a confiar en tu guía. Amén.',
                'category': 'Fe',
                'status': 'published',
            },
            {
                'title': 'El amor de Dios no tiene límites',
                'subtitle': 'Una meditación sobre el amor incondicional',
                'bible_verse': 'Juan 3:16',
                'bible_reference': 'Jn 3:16',
                'content': '''
                <h2>El amor perfecto de Dios</h2>
                <p>El amor de Dios es diferente a cualquier otro amor que podamos conocer. 
                No depende de nuestro desempeño, nuestras obras o nuestra apariencia.</p>
                
                <p>"Porque de tal manera amó Dios al mundo, que ha dado a su Hijo unigénito, 
                para que todo aquel que en él cree, no se pierda, mas tenga vida eterna." (Juan 3:16)</p>
                
                <p>Este amor es el fundamento de toda nuestra fe.</p>
                ''',
                'reflection': 'Reflexiona: ¿Cómo puedo experimentar más profundamente el amor de Dios en mi vida?',
                'prayer': 'Gracias Dios por tu amor infinito. Ayúdame a compartir ese amor con otros. Amén.',
                'category': 'Amor',
                'status': 'published',
            },
            {
                'title': 'Esperanza en medio de la adversidad',
                'subtitle': 'Encontrando luz en la oscuridad',
                'bible_verse': 'Romanos 5:3-5',
                'bible_reference': 'Rom 5:3-5',
                'content': '''
                <h2>La esperanza que no decepciona</h2>
                <p>Todos enfrentamos momentos difíciles. Pero como cristianos, 
                tenemos una esperanza que va más allá de las circunstancias.</p>
                
                <p>"Y no solo esto, sino que también nos gloriamos en nuestros sufrimientos, 
                sabiendo que el sufrimiento produce perseverancia; la perseverancia, carácter; 
                y el carácter, esperanza." (Romanos 5:3-5)</p>
                
                <p>La esperanza no es optimismo ingenuo, sino una confianza sólida en Dios.</p>
                ''',
                'reflection': 'Reflexiona: ¿Qué esperanza tienes en Dios para tu futuro?',
                'prayer': 'Señor, renueva mi esperanza hoy. Ayúdame a confiar en tu plan. Amén.',
                'category': 'Esperanza',
                'status': 'published',
            },
            {
                'title': 'Tu identidad en Cristo',
                'subtitle': 'Quién eres realmente en Dios',
                'bible_verse': '2 Corintios 5:17',
                'bible_reference': '2 Co 5:17',
                'content': '''
                <h2>Una nueva identidad</h2>
                <p>Cuando aceptamos a Jesús en nuestras vidas, nos convertimos en nuevas personas. 
                La identidad que Dios nos da es mucho más valiosa que cualquier otra.</p>
                
                <p>"De modo que si alguno está en Cristo, nueva criatura es; 
                las cosas viejas pasaron; he aquí todas son hechas nuevas." (2 Corintios 5:17)</p>
                
                <p>Tu valor no viene de lo que otros piensen, sino de ser amado por Dios.</p>
                ''',
                'reflection': 'Reflexiona: ¿Cuál es tu verdadera identidad en Cristo?',
                'prayer': 'Gracias Dios por darme una nueva identidad. Ayúdame a vivirla plenamente. Amén.',
                'category': 'Propósito',
                'status': 'published',
            },
            {
                'title': 'La paz que sobrepasa todo entendimiento',
                'subtitle': 'Encontrando calma en Dios',
                'bible_verse': 'Filipenses 4:6-7',
                'bible_reference': 'Fil 4:6-7',
                'content': '''
                <h2>Paz en la tormenta</h2>
                <p>El mundo ofrece muchas cosas, pero la verdadera paz solo viene de Dios. 
                Esta paz no depende de nuestras circunstancias.</p>
                
                <p>"Por nada estéis afanosos, sino sean conocidas vuestras peticiones delante de Dios 
                en toda oración y ruego, con acción de gracias. Y la paz de Dios, 
                que sobrepasa todo entendimiento, guardará vuestros corazones y vuestros pensamientos 
                en Cristo Jesús." (Filipenses 4:6-7)</p>
                
                <p>Esta paz es un regalo gratuito de Dios para ti.</p>
                ''',
                'reflection': 'Reflexiona: ¿Cómo puedo experimentar la paz de Dios hoy?',
                'prayer': 'Señor, llena mi corazón con tu paz. Calma mis ansiedades. Amén.',
                'category': 'Esperanza',
                'status': 'published',
            },
        ]

        devotionals_created = 0
        for dev_data in devotionals_data:
            category = categories[dev_data.pop('category')]
            dev_data['slug'] = slugify(dev_data['title'])
            dev_data['author'] = admin_user
            dev_data['publish_date'] = timezone.now()

            devotional, created = Devotional.objects.get_or_create(
                slug=dev_data['slug'],
                defaults=dev_data
            )
            devotional.category = category
            devotional.save()

            if created:
                self.stdout.write(self.style.SUCCESS(f'✅ Devocional "{dev_data["title"]}" creado'))
                devotionals_created += 1
            else:
                self.stdout.write(f'✓ Devocional "{dev_data["title"]}" ya existe')

        # Crear materiales
        materials_data = [
            {
                'title': 'Guía de lectura bíblica de 30 días',
                'description': 'Plan de lectura para conocer mejor la Palabra de Dios',
                'content': 'Un plan completo de lectura bíblica que te ayudará a leer la Biblia en 30 días.',
                'material_type': 'guide',
                'external_url': 'https://ejemplo.com/lectura-biblica',
                'is_published': True,
            },
            {
                'title': 'Estudio sobre los Salmos',
                'description': 'Un profundo análisis de los Salmos y su relevancia hoy',
                'content': 'Explora los Salmos y cómo pueden guiar tu vida espiritual.',
                'material_type': 'study',
                'external_url': 'https://ejemplo.com/salmos',
                'is_published': True,
            },
            {
                'title': 'Devocional de podcast semanal',
                'description': 'Escucha devocionales de 10 minutos cada semana',
                'content': 'Reflexiones cristianas en formato de audio para tu día.',
                'material_type': 'audio',
                'external_url': 'https://ejemplo.com/podcast',
                'is_published': True,
            },
            {
                'title': 'Biblia comentada en línea',
                'description': 'Acceso a una Biblia con comentarios detallados',
                'content': 'Comprende mejor cada versículo con comentarios académicos y devotionales.',
                'material_type': 'article',
                'external_url': 'https://ejemplo.com/biblia-comentada',
                'is_published': True,
            },
        ]

        materials_created = 0
        for mat_data in materials_data:
            mat_data['slug'] = slugify(mat_data['title'])
            mat_data['author'] = admin_user

            material, created = Material.objects.get_or_create(
                slug=mat_data['slug'],
                defaults=mat_data
            )

            if created:
                self.stdout.write(self.style.SUCCESS(f'✅ Material "{mat_data["title"]}" creado'))
                materials_created += 1
            else:
                self.stdout.write(f'✓ Material "{mat_data["title"]}" ya existe')

        self.stdout.write(self.style.SUCCESS(f'''
        
╔════════════════════════════════════════╗
║   ✅ DATOS DE PRUEBA GENERADOS        ║
╚════════════════════════════════════════╝

📊 Resumen:
  • {len(categories)} categorías creadas
  • {devotionals_created} devocionales creados
  • {materials_created} materiales creados
  
🔐 Credenciales:
  • Usuario: admin
  • Contraseña: admin123
  
🌐 Accede a:
  • Home: http://localhost:8000/
  • Admin: http://localhost:8000/admin/
  • Devocionales: http://localhost:8000/devocionales/
  • Materiales: http://localhost:8000/materiales/
        '''))

workspace {

    model {
        institucionesEducativas = person "Instituciones Educativas" "Diseñan y ofertan programas de formación. Emiten y certifican microcredenciales." {
            tags "Microsoft Azure - Administrative Units"
        }
        participantes = person "Participantes" "Adquieren aprendizajes y habilidades verificables mediante microcredenciales." {
            tags "Microsoft Azure - Users"
        }
        empleadores = person "Empleadores y Organizaciones" "Utilizan microcredenciales para validar competencias de potenciales empleados." {
            tags "Microsoft Azure - Ceres"
        }
        
        sistemasExternos = softwareSystem "Sistemas de Gestión Académica" "Permite la emisión y verificación de microcredenciales." {
            tags "Microsoft Azure - Education"
        }

        sistemaMicrocredenciales = softwareSystem "Sistema de Gestión de Microcredenciales Universitarias" "Realiza la gestión académica de los programas." {
            sistemasExternos -> this "Proporciona listados de participantes"
            institucionesEducativas -> this "Emite y certifica microcredenciales"
            participantes -> this "Usan y comparten microcredenciales"
            empleadores -> this "Verifican credenciales"
            tags "Sistema de Gestión de Microcredenciales Universitarias"
        }
    }

    views {
        systemContext sistemaMicrocredenciales {
            include *
            autolayout bt
        }
        styles {
            element "Person" {
                background #edf2f4
            }
            
            element "Sistema de Gestión de Microcredenciales Universitarias" {
                background #1b9aaa
                color #ffffff
            }

        }
        
        theme https://static.structurizr.com/themes/microsoft-azure-2023.01.24/icons.json

    }

}
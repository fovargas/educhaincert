workspace {

    model {
        // Actores externos
        institucionesEducativas = person "Instituciones Educativas" {
            tags "Microsoft Azure - Administrative Units"
        }
        participantes = person "Participantes" {
            tags "Microsoft Azure - Users"
        }
        empleadores = person "Empleadores y Organizaciones" {
            tags "Microsoft Azure - Ceres"
        }
        
        sistemasExternos = softwareSystem "Sistemas de Gestión Académica" "Permite la emisión y verificación de microcredenciales." {
            tags "Microsoft Azure - Education"
        }

        // Sistema de microcredenciales
        sistemaMicrocredenciales = softwareSystem "Sistema de Microcredenciales" {

            // Contenedor: Frontend Application
            frontendApp = container "Frontend Application" {
                // Componentes del Frontend
                djangoApp = component "Django App" "Aplicación Django para la gestión de entidades." {
                    tags "Microsoft Azure - Spot VM" "Frontend Application Element"
                }
                polymerApp = component "Polymer App" "Aplicación Polymer para la verificación de credenciales." {
                    tags "Microsoft Azure - Images" "Frontend Application Element"
                }
                mobileWallet = component "Mobile Wallet" "Aplicación móvil wallet para organizar credenciales emitidas." {
                    tags "Microsoft Azure - Mobile" "Frontend Application Element"
                }

                // Relaciones entre componentes del frontend
                djangoApp -> polymerApp "Intercambia datos para verificación de credenciales"
                djangoApp -> mobileWallet "Envía y recibe información de credenciales"
                
                tags "Frontend Application"
            }

            // Contenedor: Backend Application
            backendApp = container "Backend Application" {
                // Componentes del Backend
                pythonScripts = component "Python Scripts" "Scripts de Python usando Django para la lógica del backend." {
                    tags "Backend Application Element 0"
                }
                
                djangoModule = component "Django Module" "App en Django para la gestión de entidades." {
                    tags "Backend Application Element 1" "Microsoft Azure - Update Management Center"
                }
                
                certTools = component "Cert-Tools" "Librería de Blockcerts para la emisión de microcredenciales." {
                    tags "Backend Application Element 1" "Microsoft Azure - App Service Certificates"
                }
                certIssuer = component "Cert-Issuer" "Librería de Blockcerts para la firma de microcredenciales." {
                    tags "Backend Application Element 1" "Microsoft Azure - App Service Certificates"
                }
                certVerifier = component "Cert-Verifier" "Librería de Blockcerts para la verificación de microcredenciales." {
                    tags "Backend Application Element 1" "Microsoft Azure - App Service Certificates"
                }
                ipfsCli = component "IPFS CLI" "Herramienta de línea de comandos para el almacenamiento en IPFS." {
                    tags "Backend Application Element 1" "Microsoft Azure - Quickstart Center"
                }
                veramo = component "Veramo CLI" "Herramienta para la gestión de identidades descentralizadas." {
                    tags "Backend Application Element 1" "Microsoft Azure - Custom Azure AD Roles"
                }
                databaseModule = component "Database Module" "Módulo para gestionar las operaciones con la base de datos." {
                    tags "Backend Application Element 1" "Microsoft Azure - SQL Database"
                }
                djangoRestModule = component "Django Rest" "Módulo para construir interfaces API." {
                    tags "Backend Application Element 1" "Microsoft Azure - Analysis Services"
                }
                iaModule = component "Recommender system" "Módulo recomendador de rutas de aprendizaje." {
                    tags "Backend Application Element 1" "Microsoft Azure - Lab Accounts"
                }
                blockchainModule = component "Blockchain Module" "Módulo para gestionar transacciones con Ethereum." {
                    tags "Backend Application Element 2" "Microsoft Azure - Azure Blockchain Service"
                }

                // Relaciones entre componentes del backend
                pythonScripts -> djangoModule "Utiliza gestionar entidades del sistema"
                djangoModule -> certTools "Utiliza para crear perfiles, plantillas y genera certificados sin firmar"
                djangoModule -> certIssuer "Utiliza para firmar certificados"
                djangoModule -> certVerifier "Utiliza para verificar microcredenciales"
                djangoModule -> ipfsCli "Almacena y recupera datos de credenciales"
                djangoModule -> veramo "Gestiona identidades descentralizadas"
                djangoModule -> databaseModule "Gestiona operaciones en base de datos"
                djangoModule -> djangoRestModule "Gestiona interfaces API"
                djangoModule -> iaModule "Gestiona rutas de aprendizaje personalizadas"
                iaModule -> databaseModule "Gestiona rutas de aprendizaje en base a datos históricos"
                djangoRestModule -> databaseModule "Gestiona interfaces API a partir del modelo de base de datos"
                certIssuer -> blockchainModule "Realiza transacciones en Ethereum"
                certVerifier -> blockchainModule "Integra con Ethereum para verificación de credenciales"
            
                tags "Backend Application"
            }

            // Relaciones de los usuarios con el sistema
            institucionesEducativas -> djangoApp "Gestiona emisión de credenciales"
            participantes -> mobileWallet "Administra y presenta credenciales"
            participantes -> polymerApp "Verifica la validez de sus credenciales"
            empleadores -> polymerApp "Verifica credenciales emitidas"
            sistemasExternos -> djangoApp "Proporciona listado de participantes"
        }
    }

    views {
        
        properties {
            "structurizr.sort" "created"
        }
        
        // Vista de componentes para el Backend Application
        component backendApp {
            include *
            autolayout lr
        
        }

        // Vista de componentes para el Frontend Application
        component frontendApp {
            include *
            autolayout lr
            
        }
        
        styles {
            element "Person" {
                background #edf2f4
            }
            
            
            element "Frontend Application" {
                stroke #264653
            }
            
            
            element "Backend Application" {
                stroke #264653
            }
            
            element "Backend Application Element 0" {
                background #2364aa
                color #ffffff
            }
            
            
            element "Backend Application Element 1" {
                background #b5e2fa
            }
            
            element "Backend Application Element 2" {
                background #bde0fe
            }
            
            element "Frontend Application Element" {
                background #d3f8e2
            }

        }

        theme https://static.structurizr.com/themes/microsoft-azure-2023.01.24/icons.json
    }

}
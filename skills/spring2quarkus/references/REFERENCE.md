# Spring Boot → Quarkus Reference Guide

## Extension mapping

| Spring Boot Dependency | Quarkus Extension | Notes |
|------------------------|-------------------|-------|
| `spring-boot-starter-web` | `quarkus-resteasy-reactive` or `quarkus-resteasy` | Prefer reactive for new projects |
| `spring-boot-starter-data-jpa` | `quarkus-hibernate-orm-panache` | Active Record or Repository pattern |
| `spring-boot-starter-data-mongodb` | `quarkus-mongodb-panache` | |
| `spring-boot-starter-security` | `quarkus-security`, `quarkus-oidc` | |
| `spring-boot-starter-oauth2-resource-server` | `quarkus-oidc` | |
| `spring-boot-starter-validation` | `quarkus-hibernate-validator` | |
| `spring-boot-starter-cache` | `quarkus-cache` (Caffeine) | |
| `spring-boot-starter-actuator` | `quarkus-smallrye-health`, `quarkus-micrometer` | |
| `spring-kafka` | `quarkus-smallrye-reactive-messaging-kafka` | |
| `spring-amqp` / `spring-rabbit` | `quarkus-smallrye-reactive-messaging-rabbitmq` | |
| `spring-boot-starter-mail` | `quarkus-mailer` | |
| `spring-cloud-openfeign` | `quarkus-rest-client-reactive` | |
| `spring-boot-starter-aop` | CDI interceptors (`@Interceptor`) | |
| `spring-boot-starter-webflux` | `quarkus-resteasy-reactive` + Mutiny | Replace Reactor types with Uni/Multi |
| `spring-batch` | No direct equivalent — consider Quarkus Scheduler + custom | XL migration item |
| `spring-cloud-gateway` | Quarkus HTTP proxy / custom Vert.x route | XL migration item |

## Annotation mapping

| Spring | Quarkus / CDI / Jakarta | Notes |
|--------|------------------------|-------|
| `@RestController` | `@Path` + `@ApplicationScoped` | |
| `@GetMapping` / `@PostMapping` | `@GET` / `@POST` + `@Path` | |
| `@RequestBody` | No annotation needed (implicit in RESTEasy) | |
| `@PathVariable` | `@PathParam` | |
| `@RequestParam` | `@QueryParam` | |
| `@Service` | `@ApplicationScoped` | |
| `@Component` | `@ApplicationScoped` | |
| `@Repository` | `@ApplicationScoped` or extends `PanacheRepository` | |
| `@Configuration` + `@Bean` | `@ApplicationScoped` producer methods (`@Produces`) | |
| `@Value` | `@ConfigProperty(name = "...")` | |
| `@Autowired` | `@Inject` | |
| `@Transactional` | `@Transactional` (Jakarta) — same semantics | |
| `@Scheduled` | `@Scheduled` (Quarkus) | Slightly different syntax |
| `@Async` | Return `Uni<T>` / `CompletionStage<T>` | |
| `@EventListener` | CDI `@Observes` | |
| `@Profile` | MicroProfile Config `%profile.key=value` | |
| `@ConditionalOnProperty` | `@IfBuildProperty` / `@UnlessBuildProperty` | Build-time only |

## Configuration mapping

| Spring Boot (`application.yml`) | Quarkus (`application.properties`) |
|---------------------------------|------------------------------------|
| `server.port` | `quarkus.http.port` |
| `spring.datasource.url` | `quarkus.datasource.jdbc.url` |
| `spring.datasource.username` | `quarkus.datasource.username` |
| `spring.datasource.password` | `quarkus.datasource.password` |
| `spring.jpa.hibernate.ddl-auto` | `quarkus.hibernate-orm.database.generation` |
| `spring.jpa.show-sql` | `quarkus.hibernate-orm.log.sql` |
| `spring.security.oauth2.resourceserver.jwt.issuer-uri` | `quarkus.oidc.auth-server-url` |
| `spring.kafka.bootstrap-servers` | `kafka.bootstrap.servers` |
| `logging.level.<package>` | `quarkus.log.category."<package>".level` |
| `management.endpoints.web.exposure.include` | `quarkus.smallrye-health.ui.enable` |

## Reactive model: Reactor → Mutiny

| Project Reactor | SmallRye Mutiny |
|-----------------|-----------------|
| `Mono<T>` | `Uni<T>` |
| `Flux<T>` | `Multi<T>` |
| `.map()` | `.map()` |
| `.flatMap()` | `.flatMap()` / `.chain()` |
| `.subscribe()` | `.subscribe().with()` |
| `.block()` | `.await().indefinitely()` (avoid in production) |
| `StepVerifier` | `UniAssertSubscriber` / `@QuarkusTest` |

## T-shirt sizing quick reference

| Size | Effort    | Criteria |
|------|-----------|----------|
| XS   | 0.5–1 d/p | Mechanical change, no logic (rename, re-import) |
| S    | 1–3 d/p   | Simple rewrite with a direct equivalent |
| M    | 3–5 d/p   | Rewrite with paradigm shift or logic adaptation |
| L    | 5–10 d/p  | Complex component, multiple linked classes, integration tests |
| XL   | 10–15 d/p | Full module, cross-cutting validation, external coordination |

## Common XL/L items to flag early

- **Spring Batch** → no direct equivalent; requires redesign
- **Spring Cloud Gateway** → custom Vert.x routing or third-party API gateway
- **Spring Integration** → SmallRye Reactive Messaging covers some cases, but complex flows need redesign
- **`@ConditionalOn*` complex conditions** → Quarkus build-time only; runtime conditions require different strategies
- **Dynamic bean registration** (`BeanDefinitionRegistryPostProcessor`) → not supported in Quarkus CDI
- **Classpath scanning / custom `@ComponentScan`** → Quarkus uses build-time discovery; explicit registration may be needed

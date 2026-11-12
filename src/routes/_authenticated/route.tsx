import { createFileRoute, Outlet, redirect } from "@tanstack/react-router";
import { supabase } from "@/integrations/supabase/client";
import { ProfileDetailsGate } from "@/components/profile-details-gate";
import { DuesPrompt } from "@/components/dues-prompt";
import { MobileNav } from "@/components/mobile-nav";

export const Route = createFileRoute("/_authenticated")({
  ssr: false,
  // getSession reads the stored session locally (and finishes any OAuth code exchange). getUser would make a
  // network round trip to Supabase on every navigation. Server functions still verify the token themselves.
  beforeLoad: async () => {
    const { data } = await supabase.auth.getSession();
    if (!data.session) throw redirect({ to: "/auth" });
    return { user: data.session.user };
  },
  component: () => (<><div className="pb-[calc(3.5rem+env(safe-area-inset-bottom))] md:pb-0"><Outlet /></div><MobileNav /><ProfileDetailsGate /><DuesPrompt /></>),
});

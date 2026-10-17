"""Generate work/ShareWise_Class_Diagram.drawio from the Ex3 tactical model."""
import html, sys

OUT = sys.argv[1]
cells = []
geo = {}  # id -> (parent, x, y, w, h)
LINE, HEAD, PAD = 15, 38, 10

STY = {
    "root":   ("#DAF5F9", "#0E8FA3", "strokeWidth=2;"),
    "entity": ("#DCE8FB", "#2A63C6", ""),
    "vo":     ("#E3F4E1", "#3C8A3A", ""),
    "enum":   ("#FFF6CC", "#B8960B", ""),
    "snap":   ("#F4F4F4", "#777777", "dashed=1;"),
    "events": ("#EEE8FB", "#6A4FB3", ""),
    "ext":    ("#E7EDE8", "#55675A", "dashed=1;"),
}
STEREO = {"root": "Aggregate Root", "entity": "Entity", "vo": "Value Object", "enum": "Enumeration",
          "snap": "Snapshot", "events": "Domain Events", "ext": "External"}
CONT = {
    "core": ("#F3F6FC", "#2A63C6"), "sup": ("#FAF6EC", "#86681A"),
    "kernel": ("#F7F7F7", "#888888"), "gen": ("#F1F5F2", "#55675A"),
}


def esc_lines(lines):
    return "<br/>".join(html.escape(l) for l in lines)


def container(cid, x, y, w, h, title, kind):
    fill, stroke = CONT[kind]
    style = (f"rounded=1;arcSize=1;container=1;collapsible=0;html=1;whiteSpace=wrap;verticalAlign=top;align=left;"
             f"spacingLeft=14;spacingTop=8;fontStyle=1;fontSize=15;fillColor={fill};strokeColor={stroke};fontColor={stroke};")
    cells.append(f'<mxCell id="{cid}" value="{html.escape(title, quote=True)}" style="{style}" vertex="1" parent="1">'
                 f'<mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/></mxCell>')
    geo[cid] = ("1", x, y, w, h)


def cls(cid, parent, x, y, kind, name, attrs=(), methods=(), w=None, stereo=None):
    fill, stroke, extra = STY[kind]
    longest = max([len(l) for l in list(attrs) + list(methods)] + [len(name) + 4, 18])
    w = w or int(longest * 6.6 + 24)
    h = HEAD + (len(attrs) * LINE + PAD if attrs else 0) + (len(methods) * LINE + PAD if methods else 0)
    if not attrs and not methods:
        h = HEAD + 6
    label = (f'<p style="margin:0px;margin-top:5px;text-align:center;"><i>«{html.escape(stereo or STEREO[kind])}»</i><br/>'
             f'<b>{html.escape(name)}</b></p>')
    if attrs:
        label += f'<hr size="1" style="border-style:solid;"/><p style="margin:0px;margin-left:8px;">{esc_lines(attrs)}</p>'
    if methods:
        label += f'<hr size="1" style="border-style:solid;"/><p style="margin:0px;margin-left:8px;">{esc_lines(methods)}</p>'
    style = (f"verticalAlign=top;align=left;overflow=fill;html=1;whiteSpace=wrap;fontSize=11;fontFamily=Helvetica;"
             f"fillColor={fill};strokeColor={stroke};{extra}")
    cells.append(f'<mxCell id="{cid}" value="{html.escape(label, quote=True)}" style="{style}" vertex="1" parent="{parent}">'
                 f'<mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/></mxCell>')
    geo[cid] = (parent, x, y, w, h)
    return w, h


def note(cid, parent, x, y, w, h, text):
    style = "shape=note;whiteSpace=wrap;html=1;size=14;align=left;verticalAlign=top;spacingLeft=8;spacingTop=4;fontSize=11;fillColor=#FFFDF2;strokeColor=#B8A77A;"
    cells.append(f'<mxCell id="{cid}" value="{html.escape(text, quote=True)}" style="{style}" vertex="1" parent="{parent}">'
                 f'<mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/></mxCell>')


eid = [0]


def edge(src, tgt, style, label="", src_mult=None, tgt_mult=None, exit=None, entry=None, points=None, label_at=None):
    eid[0] += 1
    i = f"e{eid[0]}"
    floating = label if label_at is not None else None
    if floating:
        label = ""
    if exit:
        style += f"exitX={exit[0]};exitY={exit[1]};exitDx=0;exitDy=0;"
    if entry:
        style += f"entryX={entry[0]};entryY={entry[1]};entryDx=0;entryDy=0;"
    cells.append(f'<mxCell id="{i}" value="{html.escape(label, quote=True)}" style="{style}" edge="1" parent="1" source="{src}" target="{tgt}">'
                 f'<mxGeometry relative="1" as="geometry">'
                 + ('<Array as="points">' + "".join(f'<mxPoint x="{px}" y="{py}"/>' for px, py in points) + '</Array>' if points else '')
                 + '</mxGeometry></mxCell>')
    if floating:
        cells.append(f'<mxCell id="{i}l" value="{html.escape(floating)}" style="edgeLabel;html=1;fontSize=10;fontColor=#C0410D;labelBackgroundColor=#FFFFFF;" '
                     f'vertex="1" connectable="0" parent="{i}"><mxGeometry x="{label_at}" relative="1" as="geometry"><mxPoint as="offset"/></mxGeometry></mxCell>')
    for pos, m, al in ((-1, src_mult, "left"), (1, tgt_mult, "right")):
        if m:
            cells.append(f'<mxCell id="{i}{"s" if pos < 0 else "t"}" value="{html.escape(m)}" '
                         f'style="edgeLabel;resizable=0;html=1;align={al};verticalAlign=bottom;fontSize=10;labelBackgroundColor=none;" '
                         f'vertex="1" connectable="0" parent="{i}"><mxGeometry x="{0.85 * pos}" relative="1" as="geometry">'
                         f'<mxPoint x="{-4 if pos < 0 else 4}" y="-2" as="offset"/></mxGeometry></mxCell>')


BASE = "html=1;rounded=0;edgeStyle=orthogonalEdgeStyle;fontSize=10;labelBackgroundColor=#FFFFFF;"
COMP = BASE + "endArrow=diamondThin;endFill=1;endSize=14;strokeColor=#333333;"
REF = BASE + "dashed=1;endArrow=open;endFill=0;endSize=10;strokeColor=#777777;fontColor=#555555;"
DEP = BASE + "dashed=1;endArrow=open;endFill=0;endSize=10;strokeColor=#6A4FB3;fontColor=#6A4FB3;"
EVT = BASE + "endArrow=block;endFill=1;strokeWidth=1.6;strokeColor=#C0410D;fontColor=#C0410D;"

# ---------------------------------------------------------------- title + legend
note("title", "1", 0, -330, 760, 120,
     "<b style='font-size:20px'>ShareWise – tactical model (Ex3)</b><br/>"
     "Entities, value objects, aggregates and domain events per bounded context. Draft 17.10.26.<br/>"
     "Our decisions applied: Share is a VO, not the slide-64 ExpenseParticipant entity (D1) · Expense and Settlement store MemberId, not UserId (D3) · "
     "Expense checks group rules against a GroupRoster snapshot (D4) · BalanceSheet is an aggregate (D5) · Invitation is its own aggregate (D6) · "
     "SettlementPlan is computed, never stored (D7). Slides: 02.DDD 64–69, 71.")
container("leg", 1450, -330, 560, 210, "Legend", "kernel")
ly = 40
for k, txt in (("root", "Aggregate root (entity, one transaction)"), ("entity", "Entity inside an aggregate"),
               ("vo", "Value object"), ("enum", "Enumeration (also a value object)"), ("snap", "Snapshot / local copy, not an aggregate")):
    fill, stroke, extra = STY[k]
    cells.append(f'<mxCell id="lg{k}" value="{html.escape(txt)}" style="rounded=0;html=1;align=left;spacingLeft=6;fontSize=11;fillColor={fill};strokeColor={stroke};{extra}" vertex="1" parent="leg">'
                 f'<mxGeometry x="14" y="{ly}" width="250" height="24" as="geometry"/></mxCell>')
    ly += 32
for n, (sty, txt) in enumerate(((COMP, "composition (part of the aggregate)"), (REF, "reference by ID only (rule 3)"),
                                (DEP, "publishes / uses"), (EVT, "domain event, handled in its own transaction (rule 4)"))):
    y = 52 + n * 40
    cells.append(f'<mxCell id="lgt{n}" value="{html.escape(txt)}" style="text;html=1;fontSize=11;align=left;verticalAlign=middle;fillColor=none;strokeColor=none;" vertex="1" parent="leg">'
                 f'<mxGeometry x="360" y="{y - 12}" width="190" height="24" as="geometry"/></mxCell>')
    cells.append(f'<mxCell id="lge{n}" value="" style="{sty.replace("edgeStyle=orthogonalEdgeStyle;", "")}" edge="1" parent="leg">'
                 f'<mxGeometry relative="1" as="geometry"><mxPoint x="285" y="{y}" as="sourcePoint"/><mxPoint x="350" y="{y}" as="targetPoint"/></mxGeometry></mxCell>')

# ---------------------------------------------------------------- Identity (generic)
container("I", 1060, -330, 300, 150, "Identity context · generic · Keycloak (bought)", "gen")
cls("User", "I", 30, 44, "ext", "User", ["+ id: UserId", "+ email · displayName"], stereo="External · not modelled")

# ---------------------------------------------------------------- Group context
container("G", 0, 0, 1400, 760, "Group context · supporting · layered", "sup")
wi, hi = cls("Invitation", "G", 20, 60, "root", "Invitation",
             ["+ id: InvitationId", "+ groupId: GroupId", "+ invitedBy: MemberId", "+ email: EmailAddress [0..1]",
              "+ code: InvitationCode", "+ validity: ValidityPeriod", "+ status: InvitationStatus"],
             ["+ issue(groupId, inviter, email, now): MemberInvited", "+ accept(userId, now): InvitationAccepted",
              "+ decline(now): InvitationDeclined", "+ expire(now)"])
wg, hg = cls("Group", "G", 520, 60, "root", "Group",
             ["+ id: GroupId", "+ name: GroupName", "+ currency: Currency", "+ status: GroupStatus", "+ members: List<Member>"],
             ["+ create(name, currency, creator): GroupCreated, MemberJoined", "+ join(userId): MemberJoined",
              "+ leave(memberId, balance): MemberLeft", "+ removeMember(admin, memberId, balance): MemberRemoved",
              "+ promoteToAdmin(admin, memberId): MemberPromoted", "+ closeGroupForSettlement(admin): GroupClosedForSettlement",
              "+ reopenGroup(admin): GroupReopened", "+ archiveGroup(admin, allSettled): GroupArchived"])
wm, hm = cls("Member", "G", 1110, 60, "entity", "Member",
             ["+ id: MemberId", "+ userId: UserId", "+ role: MemberRole", "+ status: MemberStatus", "+ joinedAt: Instant"], w=230)
r2 = 60 + max(hi, hg) + 70
cls("InvitationStatus", "G", 20, r2, "enum", "InvitationStatus", ["PENDING", "ACCEPTED", "DECLINED", "EXPIRED"], w=160)
cls("ValidityPeriod", "G", 200, r2, "vo", "ValidityPeriod", ["+ issuedAt: Instant", "+ validUntil: Instant (+7 days)"], ["+ isExpiredAt(now): boolean"], w=220)
cls("EmailAddress", "G", 200, r2 + 140, "vo", "EmailAddress", ["+ value: String"], w=220)
cls("InvitationCode", "G", 20, r2 + 140, "vo", "InvitationCode", ["+ value: String (secret)"], w=160)
cls("GroupName", "G", 520, r2, "vo", "GroupName", ["+ value: String (1–60, not empty)"], w=220)
cls("GroupStatus", "G", 760, r2, "enum", "GroupStatus", ["OPEN", "CLOSED_FOR_SETTLEMENT", "ARCHIVED"], w=200)
cls("MemberRole", "G", 1110, r2 - 110, "enum", "MemberRole", ["ADMIN", "MEMBER"], w=110)
cls("MemberStatus", "G", 1240, r2 - 110, "enum", "MemberStatus", ["ACTIVE", "FORMER"], w=120)
cls("GroupEvents", "G", 1110, r2 + 40, "events", "Group events",
    ["GroupCreated", "MemberJoined", "MemberLeft", "MemberRemoved", "MemberPromoted", "GroupClosedForSettlement",
     "GroupReopened", "GroupArchived", "MemberInvited", "InvitationAccepted", "InvitationDeclined"], w=250)
note("nG", "G", 520, r2 + 110, 470, 96,
     "<b>Why Member is inside Group:</b> R12 (the last admin can’t leave) needs all admins in one transaction.<br/>"
     "<b>Why Invitation is separate:</b> own lifecycle + 7-day timer; inside Group every invite would lock the group (rule 2).<br/>"
     "leave() / removeMember() get the balance from Settlement (R11).")

edge("Member", "Group", COMP, "members", "1..*", "1", exit=(0, 0.3), entry=(1, 0.3))
edge("MemberRole", "Member", COMP, "", "1", None, exit=(0.5, 0), entry=(0.25, 1))
edge("MemberStatus", "Member", COMP, "", "1", None, exit=(0.5, 0), entry=(0.8, 1))
edge("GroupName", "Group", COMP, "", "1", None, exit=(0.5, 0), entry=(0.25, 1))
edge("GroupStatus", "Group", COMP, "", "1", None, exit=(0.5, 0), entry=(0.75, 1))
edge("InvitationStatus", "Invitation", COMP, "", "1", None, exit=(0.5, 0), entry=(0.2, 1))
edge("ValidityPeriod", "Invitation", COMP, "", "1", None, exit=(0.5, 0), entry=(0.6, 1))
edge("Invitation", "Group", REF, "groupId", exit=(1, 0.25), entry=(0, 0.25))
edge("Invitation", "Group", EVT, "accepted → join()", exit=(1, 0.6), entry=(0, 0.6))
edge("Member", "User", REF, "userId", exit=(0.5, 0), entry=(0.5, 1))
edge("Group", "GroupEvents", DEP, "publishes", exit=(1, 0.85), entry=(0, 0.1))

# EmailAddress / InvitationCode compositions drawn to Invitation's left edge
edge("EmailAddress", "Invitation", COMP, "", "0..1", None, exit=(1, 0.5), entry=(1, 0.95))
edge("InvitationCode", "Invitation", COMP, "", "1", None, exit=(0, 0.5), entry=(0, 0.9))

# ---------------------------------------------------------------- Expense context
EX = 1500
container("E", EX, 0, 1180, 760, "Expense context · core · hexagonal", "core")
cls("GroupRoster", "E", 20, 60, "snap", "GroupRoster",
    ["+ groupId: GroupId", "+ open: boolean", "+ currency: Currency", "+ activeMembers: Set<MemberId>", "+ admins: Set<MemberId>"],
    ["+ isActiveMember(m): boolean", "+ isAdmin(m): boolean"], w=230, stereo="Snapshot · fed by Group events (ACL)")
we, he = cls("Expense", "E", 290, 60, "root", "Expense",
             ["+ id: ExpenseId", "+ groupId: GroupId", "+ recordedBy: MemberId", "+ title: ExpenseTitle", "+ date: LocalDate",
              "+ amount: Money", "+ paidBy: MemberId", "+ split: Split", "+ status: ExpenseStatus", "+ history: List<ExpenseRevision>"],
             ["+ record(roster, recorder, title, date, amount, payer, split): ExpenseRecorded",
              "+ correct(roster, by, newVersion, reason): ExpenseCorrected", "+ remove(roster, by): ExpenseRemoved"])
cls("ExpenseEvents", "E", 290 + we + 50, 60, "events", "Expense events", ["ExpenseRecorded", "ExpenseCorrected", "ExpenseRemoved"], w=190)
note("nE", "E", 290 + we + 50, 190, 240, 150,
     "<b>Invariants inside:</b> R1 amount &gt; 0 · R3 ≥1 participant, nobody twice · R3a someone other than the payer · R4 shares = amount · R7 history kept · R8 REMOVED is final.<br/>"
     "<b>Via GroupRoster:</b> R2 R3 R5 R6 R7a.")
e2 = 60 + he + 70
cls("ExpenseTitle", "E", 20, e2, "vo", "ExpenseTitle", ["+ value: String (1–80)"], w=170)
cls("Split", "E", 220, e2, "vo", "Split", ["+ strategy: SplitStrategy", "+ shares: List<Share>"],
    ["+ equal(amount, participants): Split", "+ exact(amount, amounts): Split", "+ byPercentage(amount, percentages): Split"], w=270)
cls("ExpenseStatus", "E", 520, e2, "enum", "ExpenseStatus", ["ACTIVE", "CORRECTED", "REMOVED"], w=150)
cls("ExpenseRevision", "E", 700, e2, "vo", "ExpenseRevision",
    ["+ revision: int", "+ previous title, amount, payer, date, split", "+ correctedBy: MemberId", "+ correctedAt: Instant", "+ reason: String"], w=280)
e3 = e2 + 160
cls("Share", "E", 220, e3, "vo", "Share", ["+ participant: MemberId", "+ amount: Money", "+ percentage: Percentage [0..1]"], w=230)
cls("SplitStrategy", "E", 520, e3, "enum", "SplitStrategy", ["EQUAL", "EXACT", "PERCENTAGE"], w=150)
cls("Percentage", "E", 20, e3, "vo", "Percentage", ["+ value: BigDecimal", "  (0 < p ≤ 100)"], w=170)
note("nShare", "E", 700, e3 + 20, 280, 80,
     "<b>D1:</b> Share is a value object. The slide-64 ExpenseParticipant entity is dropped: a correction replaces the whole split, nobody tracks one share over time.")

edge("Expense", "GroupRoster", DEP, "checked against (passed in)", exit=(0, 0.3), entry=(1, 0.3))
edge("ExpenseTitle", "Expense", COMP, "", "1", None, exit=(0.5, 0), entry=(0.08, 1))
edge("Split", "Expense", COMP, "split", "1", None, exit=(0.5, 0), entry=(0.35, 1))
edge("ExpenseStatus", "Expense", COMP, "", "1", None, exit=(0.5, 0), entry=(0.65, 1))
edge("ExpenseRevision", "Expense", COMP, "history", "0..*", None, exit=(0.5, 0), entry=(0.95, 1))
edge("Share", "Split", COMP, "shares", "1..*", None, exit=(0.5, 0), entry=(0.4, 1))
edge("SplitStrategy", "Split", COMP, "", "1", None, exit=(0.5, 0), entry=(0.9, 1))
edge("Percentage", "Share", COMP, "", "0..1", None, exit=(1, 0.5), entry=(0, 0.5))
edge("Expense", "ExpenseEvents", DEP, "publishes", exit=(1, 0.2), entry=(0, 0.5))
edge("Expense", "Group", REF, "groupId (by ID)", exit=(0.5, 0), entry=(0.5, 0))
edge("GroupEvents", "GroupRoster", EVT, "Group events → update roster",
     exit=(1, 0.2), entry=(0, 0.75))

# ---------------------------------------------------------------- Settlement context
SY = 860
container("S", 0, SY, 1400, 9999, "Settlement context · core · hexagonal", "core")
wb, hb = cls("BalanceSheet", "S", 20, 60, "root", "BalanceSheet",
             ["+ groupId: GroupId  (its identity, 1 per group)", "+ currency: Currency", "+ balances: List<Balance>", "+ inSettlementPhase: boolean"],
             ["+ addMember(memberId)", "+ applyExpense(effect)", "+ replaceExpense(before, after)", "+ revertExpense(effect)",
              "+ applySettlementPayment(debtor, creditor, amount): AllBalancesSettled?",
              "+ startSettlementPhase(): AllBalancesSettled?", "+ endSettlementPhase()",
              "+ balanceOf(memberId): Money", "+ openDebtOf(m) / openCreditOf(m): Money",
              "+ calculateFinalBalances(): List<Balance>", "+ suggestSettlementPlan(): SettlementPlan"])
wp, hp = cls("SettlementPayment", "S", 600, 60, "root", "SettlementPayment",
             ["+ id: SettlementPaymentId", "+ groupId: GroupId", "+ debtor: MemberId", "+ creditor: MemberId", "+ amount: Money",
              "+ status: SettlementPaymentStatus", "+ recordedAt · decidedAt: Instant"],
             ["+ record(group, debtor, creditor, amount,", "        openDebt, openCredit): SettlementPaymentRecorded",
              "+ confirm(by): SettlementPaymentConfirmed", "+ reject(by, reason): SettlementPaymentRejected"])
s2 = 60 + max(hb, hp + 40 + 95) + 70
cls("Balance", "S", 20, s2, "vo", "Balance", ["+ member: MemberId", "+ amount: Money (±)"], ["+ isSettled(): boolean"], w=190)
cls("ExpenseEffect", "S", 240, s2, "vo", "ExpenseEffect", ["+ payer: MemberId", "+ amount: Money", "+ owed: Map<MemberId, Money>"],
    w=230, stereo="Value Object · ACL translation")
cls("SettlementPlan", "S", 500, s2, "vo", "SettlementPlan", ["+ debts: List<Debt>"], w=200, stereo="Value Object · computed, never stored")
cls("Debt", "S", 740, s2, "vo", "Debt", ["+ debtor: MemberId", "+ creditor: MemberId", "+ amount: Money"], w=190)
cls("SettlementPaymentStatus", "S", 600, 60 + hp + 40, "enum", "SettlementPaymentStatus", ["PENDING", "CONFIRMED", "REJECTED"], w=200)
cls("SettlementEvents", "S", 1080, 60, "events", "Settlement events",
    ["SettlementPaymentRecorded", "SettlementPaymentConfirmed", "SettlementPaymentRejected", "AllBalancesSettled"], w=230)
note("nS", "S", 980, s2, 330, 130,
     "<b>Invariants:</b> R14 sum of balances is always 0 · only confirmed payments count (R16) · "
     "a payment ≤ debtor’s open debt and creditor’s open credit (R17, D10) · AllBalancesSettled only in the settlement phase (L5, D8).<br/>"
     "Every aggregate holds groupId: GroupId, a reference by ID (rule 3).")

edge("Balance", "BalanceSheet", COMP, "balances", "0..*", None, exit=(0.5, 0), entry=(0.15, 1))
edge("BalanceSheet", "ExpenseEffect", DEP, "uses", exit=(0.6, 1), entry=(0.5, 0))
edge("BalanceSheet", "SettlementPlan", DEP, "creates", exit=(1, 0.85), entry=(0.5, 0))
edge("Debt", "SettlementPlan", COMP, "debts", "0..*", None, exit=(0, 0.5), entry=(1, 0.5))
edge("SettlementPaymentStatus", "SettlementPayment", COMP, "", "1", None, exit=(0.5, 0), entry=(0.3, 1))
edge("SettlementPayment", "SettlementEvents", DEP, "publishes", exit=(1, 0.2), entry=(0, 0.2))
edge("SettlementPayment", "BalanceSheet", "html=1;rounded=0;fontSize=10;dashed=1;dashPattern=1 4;endArrow=open;strokeWidth=2;strokeColor=#777777;fontColor=#555555;labelBackgroundColor=#FFFFFF;",
     "open debt / credit? (R17)", exit=(0, 0.25), entry=(1, 0.25))
edge("SettlementEvents", "BalanceSheet", EVT, "SettlementPaymentConfirmed → applySettlementPayment()", exit=(0.5, 1), entry=(0.9, 1),
     points=[(1195, SY + s2 - 35), (20 + 0.9 * wb, SY + s2 - 35)])
edge("SettlementEvents", "Group", EVT, "AllBalancesSettled → archiveGroup() (only if CLOSED, D8)", exit=(0.5, 0), entry=(1, 0.75), label_at=-0.85,
     points=[(1195, SY - 30), (1050, SY - 30), (1050, 60 + 0.75 * hg)])
edge("GroupEvents", "BalanceSheet", EVT, "GroupCreated, MemberJoined, Closed / Reopened", exit=(0.5, 1), entry=(0.8, 0),
     points=[(1235, SY - 60), (20 + 0.8 * wb, SY - 60)])
edge("ExpenseEvents", "BalanceSheet", EVT, "ExpenseRecorded / Corrected / Removed → apply / replace / revert (via ExpenseEffect)",
     exit=(1, 0.5), entry=(0.95, 0),
     points=[(EX + 1150, 60 + 0.5 * 64), (EX + 1150, SY - 80), (20 + 0.95 * wb, SY - 80)])

# ---------------------------------------------------------------- Shared kernel
container("K", EX, SY, 1180, 300, "Shared kernel · used by Expense and Settlement (context map #4b)", "kernel")
cls("Money", "K", 30, 60, "vo", "Money", ["+ amount: BigDecimal (scale 2)", "+ currency: Currency"],
    ["+ plus(Money): Money", "+ minus(Money): Money", "+ negate(): Money"], w=240)
cls("Currency", "K", 330, 60, "vo", "Currency", ["+ code: String (ISO 4217, e.g. EUR)"], w=240)
cls("TypedIds", "K", 630, 60, "vo", "Typed IDs",
    ["GroupId", "MemberId", "UserId", "ExpenseId", "InvitationId", "SettlementPaymentId", "(each wraps a UUID)"], w=220, stereo="Value Objects")
note("nK", "K", 880, 60, 270, 120,
     "Money refuses to add two different currencies (G2). One currency per group, no conversion.<br/>"
     "Typed IDs are how aggregates point at each other (slide 67, rule 3); a MemberId can’t be passed where a GroupId belongs.")
edge("Currency", "Money", COMP, "", "1", None, exit=(0, 0.5), entry=(1, 0.35))

# ---------------------------------------------------------------- Outside (read models)
container("O", EX, SY + 360, 1180, 300, "Activity (read model) · Notification (generic): listen to every event, own no aggregate", "gen")
cls("ActivityEntry", "O", 30, 60, "ext", "ActivityEntry", ["+ groupId · eventType · at · text"], w=260, stereo="Read model (CQRS, slide 78)")
cls("Notification", "O", 330, 60, "ext", "Notification", ["+ recipient · channel · text"], w=260, stereo="Generic delivery")
note("nO", "O", 630, 60, 520, 90, "Subscribes to the Group, Expense and Settlement events (Conformist, context map #6 and #7). "
     "Not part of the tactical model: no invariants, nothing changes it except incoming events.")

cells[:] = [c.replace('height="9999"', f'height="{s2 + 190}"') for c in cells]
xml = ('<mxfile host="app.diagrams.net"><diagram id="sharewise-ex3" name="ShareWise tactical model">'
       '<mxGraphModel dx="1600" dy="1000" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" '
       'page="0" pageScale="1" pageWidth="3000" pageHeight="2200" math="0" shadow="0"><root><mxCell id="0"/><mxCell id="1" parent="0"/>'
       + "".join(cells) + "</root></mxGraphModel></diagram></mxfile>")
open(OUT, "w", encoding="utf-8").write(xml)
print("cells", len(cells))
